"""
Hospital Patient Data Analyzer
Run from this folder:
    python hospital_analyzer.py
    python hospital_analyzer.py test_data/test_case_2.csv
    python hospital_analyzer.py test_data/test_case_3.csv
    python hospital_analyzer.py test_data/test_case_4.csv

Install:
    python -m pip install pandas matplotlib
"""

from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

DEFAULT_CSV = Path(__file__).with_name("patients.csv")

REQUIRED_COLUMNS = [
    "Patient_ID", "Age", "Gender", "Department",
    "Admit_Date", "Discharge_Date"
]


def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing CSV columns: {', '.join(missing_columns)}")

    original_count = len(df)

    df = df.drop_duplicates(subset="Patient_ID", keep="first").copy()
    duplicates_removed = original_count - len(df)

    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    valid_ages = df["Age"].dropna()
    if valid_ages.empty:
        raise ValueError("No valid ages found; median age cannot be calculated.")

    median_age = valid_ages.median()
    missing_age_count = int(df["Age"].isna().sum())
    df["Age"] = df["Age"].fillna(median_age)

    for column in ["Gender", "Department"]:
        df[column] = df[column].astype("string").str.strip()

    df["Admit_Date"] = pd.to_datetime(df["Admit_Date"], errors="coerce")
    df["Discharge_Date"] = pd.to_datetime(df["Discharge_Date"], errors="coerce")
    df["Length_of_Stay"] = (
        df["Discharge_Date"] - df["Admit_Date"]
    ).dt.days
    df.loc[df["Length_of_Stay"] < 0, "Length_of_Stay"] = pd.NA

    print("\n========== DATA CLEANING REPORT ==========")
    print(f"Duplicate records removed: {duplicates_removed}")
    print(f"Missing/invalid ages filled: {missing_age_count}")
    print(f"Median age used: {median_age:g}")
    print(f"Patient records available: {len(df)}")
    return df


def department_and_gender_analysis(df):
    print("\n========== DEPARTMENT-WISE PATIENT COUNT ==========")
    print(df.groupby("Department")["Patient_ID"].count().to_string())
    print(f"Total patients: {len(df)}")

    print("\n========== GENDER-WISE PATIENT COUNT ==========")
    print(df.groupby("Gender")["Patient_ID"].count().to_string())


def length_of_stay_analysis(df):
    print("\n========== LENGTH OF STAY ==========")
    valid = df.dropna(subset=["Length_of_Stay"])
    if valid.empty:
        print("No valid admission/discharge date pairs found.")
        return

    for _, patient in valid.iterrows():
        print(f"{patient['Patient_ID']}: {int(patient['Length_of_Stay'])} days")
    print(f"Average stay: {valid['Length_of_Stay'].mean():.2f} days")


def stay_and_age_group_analysis(df):
    print("\n========== STAY AND AGE GROUP ANALYSIS ==========")
    valid = df.dropna(subset=["Length_of_Stay"])
    if valid.empty:
        print("Average stay: unavailable (no valid dates)")
    else:
        print(f"Average stay: {valid['Length_of_Stay'].mean():.2f} days")

    labels = ["0-40", "41-60", "61+"]
    df = df.copy()
    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=[-1, 40, 60, float("inf")],
        labels=labels,
        right=True
    )
    counts = (
        df.groupby("Age_Group", observed=False)["Patient_ID"]
        .count()
        .reindex(labels, fill_value=0)
    )

    print("\nAge group distribution:")
    print(counts.to_string())

    counts.plot(kind="bar", title="Patients by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Number of Patients")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def main():
    csv_file = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    if not csv_file.is_absolute():
        csv_file = Path(__file__).parent / csv_file

    try:
        patients = load_and_clean_data(csv_file)
    except FileNotFoundError:
        print(f"ERROR: CSV file not found: {csv_file}")
        print("Check the filename and folder path.")
        return
    except (ValueError, pd.errors.ParserError) as error:
        print(f"ERROR: Could not process CSV: {error}")
        return

    while True:
        print("\n==========================================")
        print("       HOSPITAL PATIENT DATA ANALYZER")
        print("==========================================")
        print("1. Department-wise Patient Count")
        print("2. Calculate Length of Stay")
        print("3. Stay and Age Group Analysis")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            department_and_gender_analysis(patients)
        elif choice == "2":
            length_of_stay_analysis(patients)
        elif choice == "3":
            stay_and_age_group_analysis(patients)
        elif choice == "4":
            print("Thank you for using Hospital Patient Data Analyzer.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
