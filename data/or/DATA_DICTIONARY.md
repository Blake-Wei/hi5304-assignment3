# OR Synthetic Dataset (2025) — Data Dictionary

This synthetic dataset contains 1 full year of operating room workflow data (2025-01-01 through 2025-12-31).
Each table links via `case_id` (and outcomes/discharge also `encounter_id`).

## Tables

### or_cases.csv (one row per OR case)
- Keys: `case_id`, `encounter_id`, `patient_id`
- Context: `or_room`, `service_line`, `procedure_type`, `asa_class`, `emergent_case`, `surgeon_id`, `anesthesia_provider_id`, `anesthesia_type`
- Workflow timestamps: `scheduled_in_room_time`, `actual_in_room_time`, `incision_time`, `case_end_time`, `out_room_time`, `pacu_in_time`, `pacu_out_time`
- Durations: `case_duration_min`, `turnover_time_min`
- Delay summary: `delay_minutes`, `delay_reason`

### or_delays.csv (0–1 row per case when delayed)
- `case_id`, `delay_reason`, `delay_minutes`, `delay_severity`, `timestamp_recorded`

### anesthesia_times.csv (one row per case)
- `case_id`, `anesthesia_start_time`, `anesthesia_stop_time`, `anesthesia_duration_min`
- `airway_difficulty_score` (1–5)
- `postop_nausea_vomit_risk` (0–1)

### lab_orders.csv (0–3 rows per case)
- `lab_order_id`, `case_id`, `lab_type`
- `order_time`, `result_time`, `turnaround_time_min`
- Critical workflow: `critical_result_flag`, `critical_type`, `critical_notified_time`, `critical_notified_role`, `critical_notification_latency_min`

### nursing_vitals.csv (time series; intraop + PACU)
- `vitals_id`, `case_id`, `timestamp`, `location` (Intraop/PACU)
- `hr_bpm`, `sbp_mmHg`, `dbp_mmHg`, `spo2_percent`, `temp_c`, `pain_score_0_10`

### nursing_assessments.csv (selected documentation points)
- `assessment_id`, `case_id`, `timestamp`
- `assessment_type` (Fall Risk Score, Pain Reassessment)
- `value_numeric`, `value_text`

### secure_messages.csv (care-team communication log)
- `message_id`, `case_id`, `timestamp`, `channel`
- `sender_role`, `recipient_role`, `category`
- `response_required`, `response_time_min`

### discharge_readiness.csv (one row per case/encounter)
- `encounter_id`, `case_id`, `indicator_time`
- Indicators: `pain_controlled_flag`, `ambulation_documented_flag`, `med_reconciliation_complete_flag`,
  `followup_scheduled_flag`, `education_completed_flag`, `discharge_order_signed_flag`

### device_usage.csv (one row per case)
- `device_id`, `case_id`
- `implant_type`, `monitoring_device`
- `implant_used_flag`, `monitoring_used_flag`

### outcomes.csv (one row per case/encounter)
- `encounter_id`, `case_id`, `patient_id`
- `admission_time`, `discharge_time`, `length_of_stay_days`, `icu_required_flag`
- Discharge: `discharge_ready_score_0_1`, `discharge_barriers`
- Readmissions: `readmitted_within_30d`, `readmission_days_after_discharge`
