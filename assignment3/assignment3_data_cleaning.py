
"""
Clean both thyroid visits and measurements CSV files for Assignment 3.

This script:
1) Cleans ss_visits_thyroid_clean.csv
2) Cleans ss_measurements_timeseries.csv
3) Writes analysis-ready outputs for the team

Outputs:
- visits_analysis_ready.csv
- measurements_analysis_ready.csv
- thyroid_testing_cohort.csv
- cleaning_summary.txt

Usage:
    python assignment3_data_cleaning.py

Optional custom paths:
    python assignment3_data_cleaning.py --visits path/to/ss_visits_thyroid_clean.csv --measurements path/to/ss_measurements_timeseries.csv --outdir cleaned_output
"""

from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd


THYROID_LAB_COLS = ["tsh", "t3", "t4"]
MEASUREMENT_COLS = [
    "weight", "bmi", "triglycerides", "hba1c", "Serum_Glucose",
    "AST", "ALT", "Serum_Creatinine", "Serum_Albumin", "tsh", "t3", "t4"
]
MISSING_SENTINEL = -9999999


def make_age_group(age_series: pd.Series) -> pd.Series:
    return pd.cut(
        age_series,
        bins=[0, 17, 34, 49, 64, 120],
        labels=["0-17", "18-34", "35-49", "50-64", "65+"],
        include_lowest=True,
        right=True,
    )


def map_measurement_gender(series: pd.Series) -> pd.Series:
    mapping = {
        8532: "F",
        8507: "M",
        0: "Unknown",
    }
    return series.map(mapping).fillna("Unknown")


def map_measurement_race(series: pd.Series) -> pd.Series:
    mapping = {
        8527: "White",
        8516: "Black or African American",
        8515: "Asian",
        8657: "Native Hawaiian or Other Pacific Islander",
        8557: "American Indian or Alaska Native",
        0: "Unknown",
    }
    return series.map(mapping).fillna("Other")


def map_measurement_ethnicity(series: pd.Series) -> pd.Series:
    mapping = {
        38003564: "Not Hispanic or Latino",
        38003563: "Hispanic or Latino",
        0: "Unknown",
    }
    return series.map(mapping).fillna("Other")


def standardize_visit_type(vt: pd.Series) -> pd.Series:
    vt = vt.fillna("Unknown").astype(str).str.strip()

    office_like = {"Office Visit", "Outpatient Visit"}
    inpatient_like = {"Inpatient Visit", "Inpatient Hospital", "Emergency Room and Inpatient Visit"}
    emergency_like = {"Emergency Room Visit", "Emergency Room and Inpatient Visit"}
    telehealth_like = {"Telehealth Provided Other than in Patients Home"}

    grouped = pd.Series(index=vt.index, dtype="object")
    grouped.loc[vt.isin(office_like)] = "Office/Outpatient"
    grouped.loc[vt.isin(inpatient_like)] = "Inpatient-Related"
    grouped.loc[vt.isin(emergency_like)] = "Emergency-Related"
    grouped.loc[vt.isin(telehealth_like)] = "Telehealth"
    grouped.loc[vt.eq("Case Management Agency")] = "Case Management"
    grouped = grouped.fillna("Other")
    return grouped


def clean_visits(visits_path: Path) -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(visits_path)
    original_rows = len(df)

    # Basic text cleanup
    text_cols = ["gender", "race", "ethnicity", "condition_description", "visit_type"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    # Convert obvious string placeholders to missing
    df.replace({"nan": np.nan, "None": np.nan, "": np.nan}, inplace=True)

    # Parse dates
    df["visit_start_date"] = pd.to_datetime(df["visit_start_date"], errors="coerce")
    df["visit_end_date"] = pd.to_datetime(df["visit_end_date"], errors="coerce")

    # Clean year_of_birth and derive age
    df["year_of_birth"] = pd.to_numeric(df["year_of_birth"], errors="coerce")
    df.loc[(df["year_of_birth"] < 1900) | (df["year_of_birth"] > 2026), "year_of_birth"] = np.nan
    df["age_at_visit"] = df["visit_start_date"].dt.year - df["year_of_birth"]
    df.loc[(df["age_at_visit"] < 0) | (df["age_at_visit"] > 120), "age_at_visit"] = np.nan
    df["age_group"] = make_age_group(df["age_at_visit"])

    # Duration
    df["visit_duration_days"] = (df["visit_end_date"] - df["visit_start_date"]).dt.days
    df.loc[df["visit_duration_days"] < 0, "visit_duration_days"] = np.nan
    df["same_day_visit_flag"] = np.where(df["visit_duration_days"].eq(0), 1, 0)
    df["long_visit_flag_7d"] = np.where(df["visit_duration_days"] > 7, 1, 0)
    df["long_visit_flag_30d"] = np.where(df["visit_duration_days"] > 30, 1, 0)

    # Standardized categories
    df["gender_clean"] = df["gender"].replace({"Other": "Other/Unknown"}).fillna("Other/Unknown")
    df["race_clean"] = df["race"].fillna("Unknown")
    df["ethnicity_clean"] = df["ethnicity"].fillna("Unknown")
    df["condition_description_clean"] = df["condition_description"].fillna("Unknown")
    df["visit_type_clean"] = df["visit_type"].fillna("Unknown")
    df["visit_type_group"] = standardize_visit_type(df["visit_type_clean"])

    # Helper flags for analysis
    df["office_related_flag"] = df["visit_type_group"].eq("Office/Outpatient").astype(int)
    df["inpatient_related_flag"] = df["visit_type_group"].eq("Inpatient-Related").astype(int)
    df["emergency_related_flag"] = df["visit_type_group"].eq("Emergency-Related").astype(int)
    df["telehealth_flag"] = df["visit_type_group"].eq("Telehealth").astype(int)

    # Keep a consistent column order
    ordered_cols = [
        "person_id",
        "gender_concept_id", "gender", "gender_clean",
        "year_of_birth", "age_at_visit", "age_group",
        "race", "race_clean", "ethnicity", "ethnicity_clean",
        "snomed_condition_concept_id", "condition_description", "condition_description_clean",
        "visit_concept_id", "visit_type", "visit_type_clean", "visit_type_group",
        "visit_start_date", "visit_end_date", "visit_duration_days",
        "same_day_visit_flag", "long_visit_flag_7d", "long_visit_flag_30d",
        "office_related_flag", "inpatient_related_flag", "emergency_related_flag", "telehealth_flag",
    ]
    df = df[ordered_cols]

    summary = {
        "original_rows": original_rows,
        "cleaned_rows": len(df),
        "unique_people": int(df["person_id"].nunique()),
        "rows_with_age": int(df["age_at_visit"].notna().sum()),
        "rows_with_duration": int(df["visit_duration_days"].notna().sum()),
        "inpatient_related_rows": int(df["inpatient_related_flag"].sum()),
        "emergency_related_rows": int(df["emergency_related_flag"].sum()),
        "office_related_rows": int(df["office_related_flag"].sum()),
    }
    return df, summary


def clean_measurements(measurements_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    df = pd.read_csv(measurements_path)
    original_rows = len(df)

    # Parse dates
    df["measurement_date"] = pd.to_datetime(df["measurement_date"], errors="coerce")

    # Clean numeric columns and sentinel missing values
    for col in MEASUREMENT_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df[col] == MISSING_SENTINEL, col] = np.nan

    # Demographic mappings
    df["gender_clean"] = map_measurement_gender(df["gender_concept_id"])
    df["race_clean"] = map_measurement_race(df["race_concept_id"])
    df["ethnicity_clean"] = map_measurement_ethnicity(df["ethnicity_concept_id"])

    # Clean year_of_birth and derive age
    df["year_of_birth"] = pd.to_numeric(df["year_of_birth"], errors="coerce")
    df.loc[(df["year_of_birth"] < 1900) | (df["year_of_birth"] > 2026), "year_of_birth"] = np.nan
    df["age_at_measurement"] = df["measurement_date"].dt.year - df["year_of_birth"]
    df.loc[(df["age_at_measurement"] < 0) | (df["age_at_measurement"] > 120), "age_at_measurement"] = np.nan
    df["age_group"] = make_age_group(df["age_at_measurement"])

    # Time helpers
    df["measurement_year"] = df["measurement_date"].dt.year
    df["measurement_month"] = df["measurement_date"].dt.to_period("M").astype("string")

    # Flags for presence of labs
    for col in THYROID_LAB_COLS:
        df[f"has_{col}"] = df[col].notna().astype(int)
    df["has_any_thyroid_test"] = df[THYROID_LAB_COLS].notna().any(axis=1).astype(int)

    # Simple value cleaning for impossible negatives
    nonnegative_cols = [
        "weight", "bmi", "triglycerides", "hba1c", "Serum_Glucose",
        "AST", "ALT", "Serum_Creatinine", "Serum_Albumin", "tsh", "t3", "t4"
    ]
    for col in nonnegative_cols:
        df.loc[df[col] < 0, col] = np.nan

    # Thyroid testing cohort: keep one earliest test row per person
    testing = (
        df.loc[df["has_any_thyroid_test"].eq(1)]
        .sort_values(["person_id", "measurement_date"])
        .drop_duplicates(subset=["person_id"], keep="first")
        .copy()
    )

    ordered_cols = [
        "person_id",
        "gender_concept_id", "gender_clean",
        "year_of_birth", "age_at_measurement", "age_group",
        "race_concept_id", "race_clean",
        "ethnicity_concept_id", "ethnicity_clean",
        "measurement_date", "measurement_year", "measurement_month",
        "weight", "bmi", "triglycerides", "hba1c", "Serum_Glucose",
        "AST", "ALT", "Serum_Creatinine", "Serum_Albumin",
        "tsh", "t3", "t4",
        "has_tsh", "has_t3", "has_t4", "has_any_thyroid_test",
    ]
    df = df[ordered_cols]
    testing = testing[ordered_cols]

    summary = {
        "original_rows": original_rows,
        "cleaned_rows": len(df),
        "unique_people": int(df["person_id"].nunique()),
        "rows_with_any_thyroid_test": int(df["has_any_thyroid_test"].sum()),
        "unique_people_with_any_thyroid_test": int(testing["person_id"].nunique()),
        "rows_with_age": int(df["age_at_measurement"].notna().sum()),
    }
    return df, testing, summary


def write_summary(path: Path, visits_summary: dict, measurements_summary: dict) -> None:
    lines = []
    lines.append("Assignment 3 cleaning summary")
    lines.append("=" * 40)
    lines.append("")
    lines.append("Visits dataset")
    for k, v in visits_summary.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("Measurements dataset")
    for k, v in measurements_summary.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("Notes")
    lines.append("- The two datasets were cleaned separately and should not be force-joined at the patient level for analysis.")
    lines.append("- year_of_birth values outside 1900-2026 were set to missing before age was calculated.")
    lines.append("- visit_duration_days was set to missing when visit_end_date occurred before visit_start_date.")
    lines.append("- In the measurements file, -9999999 was treated as missing for lab/body-measurement fields.")
    lines.append("- thyroid_testing_cohort.csv keeps the earliest row per person with a non-missing TSH, T3, or T4.")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--visits", default="ss_visits_thyroid_clean.csv")
    parser.add_argument("--measurements", default="ss_measurements_timeseries.csv")
    parser.add_argument("--outdir", default=".")
    args = parser.parse_args()

    visits_path = Path(args.visits)
    measurements_path = Path(args.measurements)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    visits_clean, visits_summary = clean_visits(visits_path)
    measurements_clean, testing_cohort, measurements_summary = clean_measurements(measurements_path)

    visits_clean.to_csv(outdir / "visits_analysis_ready.csv", index=False)
    measurements_clean.to_csv(outdir / "measurements_analysis_ready.csv", index=False)
    testing_cohort.to_csv(outdir / "thyroid_testing_cohort.csv", index=False)
    write_summary(outdir / "cleaning_summary.txt", visits_summary, measurements_summary)

    print("Cleaning complete.")
    print(f"Saved: {outdir / 'visits_analysis_ready.csv'}")
    print(f"Saved: {outdir / 'measurements_analysis_ready.csv'}")
    print(f"Saved: {outdir / 'thyroid_testing_cohort.csv'}")
    print(f"Saved: {outdir / 'cleaning_summary.txt'}")


if __name__ == "__main__":
    main()
