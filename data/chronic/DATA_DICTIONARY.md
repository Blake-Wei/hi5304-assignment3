# Chronic Disease Management: Diabetes and Hypertension — Synthetic Dataset (2024–2025)

**Primary purpose:** teaching longitudinal disease progression, outcomes research, utilization, and population stratification in diabetes and hypertension.

Time range: **2024-01-01 to 2025-12-31** (>= 2 years).  
Patients have an `index_date` in 2024 H1 to ensure longitudinal follow-up.

## Keys
- `patient_id` joins all tables.
- `appointment_id` links `appointments.csv` → `visits.csv` (when not missed).
- `visit_id` links to `bp_readings.csv` and `nursing_documentation.csv` (clinic measurements/docs).
- `encounter_id` unique in `encounters.csv`; `stay_id` unique in `inpatient_stays.csv`.

## Tables

### patients.csv
- Demographics + insurance + geography: `dob`, `sex`, `race`, `ethnicity`, `insurance`, `urbanicity`, `zip3`
- Cohort: `cohort` ∈ (Diabetes only, Hypertension only, Both)
- Social risk: `sdoh_risk_score_0_10`
- `index_date` first chronic condition date (synthetic)

### diagnoses.csv
- ICD-10 for diabetes (`E11.9`), hypertension (`I10`), and hyperlipidemia (`E78.5`) subset
- Fields: `dx_id`, `dx_date`, `icd10_code`, `dx_group`

### sdoh_screenings.csv / sdoh_zcode_diagnoses.csv
- Baseline + annual screenings at domain level (`positive_flag`, `severity`)
- Z-code diagnoses recorded for many positives

### appointments.csv
- Scheduled chronic care appointments (quarterly-ish)
- `missed_flag` + `cancel_reason` when missed

### visits.csv
- Completed visits only (created when appointment not missed)
- `visit_setting` includes Primary Care, Endocrinology, Cardiology, Nurse Visit

### bp_readings.csv
- BP trends over time: clinic readings at visits + monthly home readings for a subset
- `setting` ∈ Clinic/Home

### labs.csv
- A1c quarterly for diabetes cohorts
- Fasting glucose monthly for a subset of diabetes patients
- Lipid components annually (LDL/HDL/TG) for most

### medications.csv
- Medication list snapshots at index and ~12 months
- Includes basic adherence proxy `adherence_estimate_0_1`

### nursing_documentation.csv
- Foot exams (diabetes cohorts) and self-management education topics

### preventive_screenings.csv
- Preventive care events; rates vary by insurance and SDOH
- Includes diabetes-specific items (retinal, nephropathy) more common in diabetes cohorts

### vaccinations.csv
- Influenza (yearly) + other vaccines (COVID-19, pneumococcal, Hep B, shingles)

### encounters.csv / inpatient_stays.csv
- ED and inpatient utilization + inpatient LOS, ICU flag
- Readmissions within 30 days in `inpatient_stays.csv`

### patient_year_summary.csv (optional convenience)
- Per patient-year: missed appointment counts + ED visits + admissions/readmissions + average LOS

## Supports sample questions
- Trends: join `patients` to `labs` (A1c/glucose) and `bp_readings` over time.
- Missed appointments: `appointments` (missed_flag) vs `encounters`/`inpatient_stays` and labs/BP trends.
- Preventive care + vaccines by insurance/SDOH: `preventive_screenings`, `vaccinations` grouped by `patients.insurance` and SDOH indicators.
