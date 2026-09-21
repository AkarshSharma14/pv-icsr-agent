# app.py

import streamlit as st
from sample_data import SAMPLE_CASES
from agent_logic import triage_icsr_source_text

st.set_page_config(page_title="PV AI-Agent: ICSR Triage & Coding", layout="wide")

st.title("🛡️ PV-AI Agent: Automated ICSR Triage, Coding & Narrative Draft")
st.caption("Enterprise Pharmacovigilance Intake & Regulatory Coding Simulation | Powered by Gemini API & Pydantic")

st.sidebar.header("Case Selector")
selected_sample = st.sidebar.selectbox("Choose a Sample Case:", list(SAMPLE_CASES.keys()))

col_input, col_output = st.columns([1, 1])

with col_input:
    st.subheader("Source Document Intake")

    raw_text = st.text_area(
        "Paste Medical Note / Physician Email / Call Log:",
        value=SAMPLE_CASES[selected_sample],
        height=200
    )

    uploaded_file = st.file_uploader(
        "Or upload a scanned medical image (PNG/JPG):",
        type=["png", "jpg", "jpeg"]
    )

    image_bytes = None
    mime_type = None

    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
        mime_type = uploaded_file.type
        st.image(uploaded_file, caption="Uploaded Document Preview", use_container_width=True)

    process_btn = st.button("🚀 Process & Triage Case", type="primary", use_container_width=True)

with col_output:
    st.subheader("Automated Case Analytics")

    if process_btn:
        if not raw_text and not uploaded_file:
            st.warning("Please paste text or upload an image to process.")
        else:
            with st.spinner("Processing case criteria, MedDRA/WHO-DD coding, and narrative..."):
                try:
                    triage_res = triage_icsr_source_text(
                        source_text=raw_text,
                        image_bytes=image_bytes,
                        mime_type=mime_type
                    )

                    val_col, ser_col = st.columns(2)

                    with val_col:
                        if triage_res.is_valid_icsr:
                            st.success("✅ **VALID ICSR**: Day 0 Set")
                        else:
                            st.error("❌ **INVALID ICSR**: Missing Criteria")

                    with ser_col:
                        if triage_res.is_serious:
                            st.error(f"🚨 **SERIOUS**: {triage_res.seriousness_criteria}")
                        else:
                            st.info("ℹ️ **NON-SERIOUS CASE**")

                    tab1, tab2, tab3, tab4 = st.tabs([
                        "📊 4-Criteria Triage",
                        "🏷️ MedDRA & WHO-DD Coding",
                        "📝 Safety Narrative",
                        "🔍 Audit Trail"
                    ])

                    with tab1:
                        m1, m2 = st.columns(2)
                        m3, m4 = st.columns(2)

                        m1.metric("1. Patient", "Identified" if triage_res.has_identifiable_patient else "Missing",
                                  triage_res.patient_details)
                        m2.metric("2. Reporter", "Identified" if triage_res.has_identifiable_reporter else "Missing",
                                  triage_res.reporter_details)
                        m3.metric("3. Suspect Drug", "Identified" if triage_res.has_suspect_drug else "Missing",
                                  triage_res.suspect_drug_details)
                        m4.metric("4. Adverse Event", "Identified" if triage_res.has_adverse_event else "Missing",
                                  triage_res.adverse_event_details)

                    with tab2:
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown("### 🧬 MedDRA AE Coding")
                            st.write(f"**Lowest Level Term (LLT):** `{triage_res.meddra_llt}`")
                            st.write(f"**Preferred Term (PT):** `{triage_res.meddra_pt}`")
                            st.write(f"**System Organ Class (SOC):** `{triage_res.meddra_soc}`")

                        with c2:
                            st.markdown("### 💊 WHO Drug Dictionary")
                            st.write(f"**Trade Name:** `{triage_res.who_drug_name}`")
                            st.write(f"**Active Ingredient:** `{triage_res.who_active_ingredient}`")
                            st.write(f"**ATC Code:** `{triage_res.who_atc_code}`")
                            st.write(f"**ATC Class:** `{triage_res.who_atc_description}`")

                    with tab3:
                        st.markdown(triage_res.safety_narrative)

                    with tab4:
                        st.markdown("**LLM Triage & Coding Reasoning Log:**")
                        st.info(triage_res.triage_reasoning)

                except Exception as e:
                    st.error(f"Error processing case: {e}")