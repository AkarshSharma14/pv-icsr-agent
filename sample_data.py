# sample_data.py

SAMPLE_CASES = {
    "Case 1: Complete Valid ICSR (Physician Email)": """
From: Dr. Aris Sharma <asharma@cityhospital.org>
To: Safety Dept <pv-intake@pharma.com>
Date: Sep 19, 2026
Subject: Adverse Event Report - Sertraline

Dear Safety Team,
I am reporting an adverse event for my 45-year-old male patient (Initials: J.D.). 
He started taking Sertraline 50mg daily on Sep 1, 2026. On Sep 10, he developed 
a severe generalised skin rash and high fever (102°F). 

Sertraline was immediately discontinued on Sep 12. Following withdrawal, the rash 
began to subside over the next 48 hours (positive dechallenge).

Regards,
Dr. Aris Sharma, MD
    """,

    "Case 2: Invalid Case (Missing Patient Info)": """
Spontaneous report received via customer helpline:
A patient reported experiencing severe nausea and vomiting after taking 20mg Omeprazole 
for acid reflux. The caller did not provide their age, gender, initials, or contact details, 
and hung up before the agent could gather demographic information.
    """,

    "Case 3: Invalid Case (Missing Suspect Drug)": """
From: Nurse Sarah Jenkins <sjenkins@clinic.org>
Patient: 62-year-old female (Initials: M.R.)
Event: Experienced sudden anaphylactic reaction and hives requiring epinephrine.
Note: Patient was recently started on a new antihypertensive medication last week, 
but the specific name and dosage of the drug were not recorded in the intake chart.
    """,

    "Case 4: Ambiguous PSP Report (Needs Narrative Polish)": """
Patient Support Program Call Log:
Caller J.K. (34yo female) taking Drug X 100mg for Rheumatoid Arthritis. Started 3 months ago.
Mentions having sore throat and fatigue since Monday. Unsure if related to drug or flu season.
Doctor told her to keep taking it for now.
    """
}