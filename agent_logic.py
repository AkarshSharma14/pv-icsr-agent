# agent_logic.py

import os
import time
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


class ICSRTriageSchema(BaseModel):
    # 4 Minimum Criteria
    has_identifiable_patient: bool = Field(description="True if patient age, gender, initials, or ID exist.")
    patient_details: str = Field(description="Extracted patient demographics or 'Missing'")

    has_identifiable_reporter: bool = Field(description="True if reporter name, title, or contact exist.")
    reporter_details: str = Field(description="Extracted reporter information or 'Missing'")

    has_suspect_drug: bool = Field(description="True if a specific drug/medication name is identified.")
    suspect_drug_details: str = Field(description="Extracted suspect drug name and dosage or 'Missing'")

    has_adverse_event: bool = Field(description="True if a clear adverse reaction/symptom is reported.")
    adverse_event_details: str = Field(description="Extracted adverse event(s) or 'Missing'")

    is_valid_icsr: bool = Field(description="True ONLY if ALL 4 criteria above are present.")

    # ICH E2A Seriousness
    is_serious: bool = Field(
        description="True if event involves death, hospitalization, life-threatening outcome, disability, or congenital anomaly.")
    seriousness_criteria: str = Field(
        description="Specify criteria met (e.g. Hospitalization, Life-threatening) or 'Non-Serious'")

    # MedDRA Coding
    meddra_llt: str = Field(description="MedDRA Lowest Level Term (LLT)")
    meddra_pt: str = Field(description="MedDRA Preferred Term (PT)")
    meddra_soc: str = Field(description="MedDRA System Organ Class (SOC)")

    # WHO Drug Dictionary Coding
    who_drug_name: str = Field(description="WHO-DD Standardized Drug Trade/Medicinal Product Name")
    who_active_ingredient: str = Field(description="Active Pharmaceutical Ingredient (API)")
    who_atc_code: str = Field(description="Anatomical Therapeutic Chemical (ATC) Code")
    who_atc_description: str = Field(description="ATC Class Description")

    triage_reasoning: str = Field(
        description="Audit explanation for validity, seriousness, and dictionary coding choices.")

    # Single-pass Safety Narrative
    safety_narrative: str = Field(
        description="If valid ICSR, draft a standard 3-paragraph safety narrative including MedDRA PT and WHO ATC code. If invalid, state that narrative drafting is halted pending follow-up.")


def _call_gemini_with_retry(contents, response_schema=None, temperature=0.1):
    """Fast-fail call to Gemini. Max 1 retry with a 1-second delay to avoid UI hanging."""
    models_to_try = ["gemini-3.6-flash", "gemini-flash-latest"]
    last_exception = None

    for model_name in models_to_try:
        for attempt in range(2):  # Max 2 attempts per model
            try:
                config_args = {"temperature": temperature}
                if response_schema:
                    config_args["response_mime_type"] = "application/json"
                    config_args["response_schema"] = response_schema

                return client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(**config_args)
                )
            except Exception as e:
                last_exception = e
                err_msg = str(e)

                # Skip to next model immediately if standard 404
                if "404" in err_msg or "NOT_FOUND" in err_msg:
                    break

                # Quick 1s pause if server busy or rate limited
                if ("503" in err_msg or "UNAVAILABLE" in err_msg or "429" in err_msg) and attempt == 0:
                    time.sleep(1)
                    continue
                break

    # Format 503 error cleanly for UI if Google API servers are overloaded
    if "503" in str(last_exception) or "UNAVAILABLE" in str(last_exception):
        raise Exception(
            "⚡ Google API server is experiencing temporary high demand (503). Please wait 5–10 seconds and click 'Process & Triage Case' again.")

    raise Exception(f"Gemini API Error: {last_exception}")


def triage_icsr_source_text(source_text: str = "", image_bytes: Optional[bytes] = None,
                            mime_type: Optional[str] = None) -> ICSRTriageSchema:
    prompt = f"""
    You are an expert Pharmacovigilance Medical Coder, Triage Agent, and Medical Writer.
    Analyze the provided medical document and complete all tasks in a single evaluation:
    1. Evaluate the 4 minimum ICSR criteria (Patient, Reporter, Suspect Drug, Adverse Event).
    2. Evaluate ICH E2A Seriousness criteria.
    3. MedDRA Coding: Assign LLT, PT, and SOC.
    4. WHO Drug Dictionary Coding: Assign Standard Product Name, Active Ingredient, ATC Code, and ATC Description.
    5. Safety Narrative: Draft a 3-paragraph ICSR narrative if valid. If invalid, state narrative generation is halted.

    Text Context (if any):
    {source_text}
    """

    contents = [prompt]
    if image_bytes and mime_type:
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))

    response = _call_gemini_with_retry(
        contents=contents,
        response_schema=ICSRTriageSchema,
        temperature=0.1
    )

    return ICSRTriageSchema.model_validate_json(response.text)
