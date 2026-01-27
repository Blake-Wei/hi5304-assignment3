# Longitudinal Oncology Patient Profiles — Synthetic Dataset (2023–2025)

**Primary purpose:** teaching longitudinal disease progression, outcomes research, utilization, and population stratification.

- All utilization/proxy outcomes occur between **2023-01-01 and 2025-12-31**.
- Patients have an **index diagnosis date** between **2023-01-01 and 2024-06-30** (18–36 months follow-up).
- Higher `sdoh_risk_score_0_10` increases simulated ED use, inpatient stays, readmissions, and symptom burden.

## Keys
- `patient_id` joins all tables.
- `encounter_id` is unique in `encounters.csv`.
- `stay_id` is unique in `inpatient_stays.csv` and references the ED trigger via `index_encounter_id`.

## Tables

### patients.csv (one row per patient)
Demographics + cancer type and stage + baseline SDOH risk:
- `patient_id`, `dob`, `sex`, `race`, `ethnicity`
- `insurance`, `urbanicity`, `zip3`
- `index_dx_date`, `primary_cancer_type`, `primary_onc_icd10`, `stage_at_dx`
- `sdoh_risk_score_0_10`, `lost_to_followup_flag`

### oncology_diagnoses.csv
Oncology-related ICD-10 codes:
- Primary cancer ICD-10 per patient
- Stage IV includes a metastasis code (`C79.9`)
- Subset includes a treatment toxicity code (neutropenia proxy)

### comorbidities.csv
Common comorbid conditions (ICD-10) with onset dates:
- HTN, T2DM, COPD, CHF, CKD, Depression, Obesity, CAD

### sdoh_screenings.csv
Long format SDOH screening data (baseline + annual):
- `domain`, `positive_flag`, `severity`

### sdoh_zcode_diagnoses.csv
ICD-10 Z-codes for positive screens:
- one row per recorded positive domain

### patient_reported_outcomes.csv
Quarterly PROs (long format), with more symptom burden during first 6 months:
- `pro_type` ∈ Pain Interference, Fatigue, Physical Function, Anxiety, Depression
- `score_0_100` (higher worse for symptoms; higher better for Physical Function)
- Missingness slightly higher with high SDOH

### encounters.csv
All encounters (scheduled + unscheduled):
- `encounter_type` ∈ Outpatient Oncology, Emergency Department, Inpatient
- `scheduled_flag` for planned oncology visits
- flags: `ed_flag`, `inpatient_flag`

### inpatient_stays.csv
Inpatient stays with readmissions:
- `admit_datetime`, `discharge_datetime`, `length_of_stay_days`, `icu_flag`
- `readmitted_within_30d`, `readmission_stay_id`, `days_to_readmission`

### patient_year_summary.csv (optional convenience)
Pre-aggregated utilization per patient-year:
- oncology visits, ED visits, inpatient encounters/stays, readmissions, avg LOS
Plus baseline stratifiers (stage, cancer type, insurance, SDOH risk)

## Supports sample questions
- SDOH → utilization/readmissions: join `patients` with `encounters` / `inpatient_stays` and/or use `patient_year_summary`.
- Care trajectory: sequence outpatient oncology visits with ED/inpatient events by time since `index_dx_date`.
- Comorbidities → ED visits during treatment: count ED visits in first 180 days post-index, stratify by CHF/COPD/CKD and stage.
