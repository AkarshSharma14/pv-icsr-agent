# 🛡️ AI Pharmacovigilance (PV) Agent: Automated ICSR Triage, Dictionary Coding & Safety Narrative Drafting

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pv-icsr-agent-sm7qwrvzuisectgysx77k.streamlit.app)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Gemini API](https://img.shields.io/badge/Google%20GenAI-Gemini%203.6%20Flash-orange.svg)
![Pydantic](https://img.shields.io/badge/Validation-Pydantic%20v2-green.svg)

An enterprise-grade **Pharmacovigilance (PV) Intake & Regulatory Processing Simulation** designed to automate initial case processing for Individual Case Safety Reports (ICSRs). Powered by the Google GenAI SDK (`gemini-3.6-flash`) and Pydantic for deterministic JSON schema enforcement, this agent evaluates regulatory validity, determines ICH E2A seriousness criteria, maps terms to MedDRA/WHO-DD dictionaries, and drafts standard safety narratives in a single pass.

👉 **[Live Interactive Demo](https://pv-icsr-agent-sm7qwrvzuisectgysx77k.streamlit.app)**

---

## 🌟 Key Capabilities

1. **Automated 4 Minimum Criteria Triage (Day 0 Identification):**
   * Instant validation of mandatory regulatory intake criteria: *Identifiable Patient*, *Identifiable Reporter*, *Suspect Drug/Biological*, and *Adverse Event*.
   * Sets the Day 0 clock automatically upon full criteria fulfillment.

2. **ICH E2A Seriousness Assessment:**
   * Evaluates incoming medical narratives against standardized regulatory seriousness criteria (*Death, Life-Threatening, Inpatient Hospitalization, Persistent Disability, Congenital Anomaly, or Medically Important Event*).

3. **Regulatory Dictionary Coding:**
   * **MedDRA Coding:** Standardizes reported signs and symptoms into Lowest Level Term (LLT), Preferred Term (PT), and System Organ Class (SOC).
   * **WHO Drug Dictionary (WHO-DD):** Standardizes suspect drugs to active ingredients and Anatomical Therapeutic Chemical (ATC) classification codes.

4. **Automated Safety Narrative Drafting:**
   * Generates structured 3-paragraph regulatory safety narratives synthesizing patient background, suspect medication exposure, clinical event timelines, intervention, and outcome.

5. **Multimodal Case Processing (Text & Vision OCR):**
   * Accepts unstructured clinical text (physician notes, call logs, emails) and scanned medical records/images (`.png`, `.jpg`) via Gemini's multimodal visual parser.

6. **Fault-Tolerant Enterprise Architecture:**
   * Single-pass execution for minimal latency (~3–5 seconds).
   * Built-in exponential backoff retries handling Google API rate limits (`429`) and temporary high-demand spikes (`503`).

---

## 🛠️ Architecture & Tech Stack

```text
+-----------------------------------------------------------------------+
|                        Streamlit UI Layer                             |
|           (Multimodal Text & Image Input Intake Dashboard)            |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                   Backend Orchestration Layer                         |
|              (Single-Pass Execution + Exponential Retry Logic)        |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                       Google GenAI API Engine                         |
|   (gemini-3.6-flash + Pydantic Schema Enforcement for Structured JSON)  |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                        Validated ICSR Output                          |
|  (Day 0 Triage | ICH Seriousness | MedDRA/WHO-DD | Safety Narrative)  |
+-----------------------------------------------------------------------+

Frontend: Streamlit

AI Engine: Google GenAI SDK (google-genai using gemini-3.6-flash)

Validation: Pydantic v2 for strict JSON output structure

Secrets Management: Native Streamlit Cloud Secrets (Zero key exposure)
