# Hospital Patient Data Analyzer

## Included files
- `hospital_analyzer.py` — main Python program
- `patients.csv` — default sample data (Test Case 1)
- `test_data/test_case_1_normal.csv` — normal input
- `test_data/test_case_2_boundary.csv` — one patient, same-day discharge
- `test_data/test_case_3_invalid.csv` — duplicate Patient_ID and missing age
- `test_data/test_case_4_age_groups.csv` — data for age-group chart test

## 1. Install libraries
Open the VS Code terminal in this folder and run:

```bash
python -m pip install pandas matplotlib
```

## 2. Run the default project
```bash
python hospital_analyzer.py
```

## 3. Run each test file
Run one command at a time:

```bash
python hospital_analyzer.py test_data/test_case_1_normal.csv
python hospital_analyzer.py test_data/test_case_2_boundary.csv
python hospital_analyzer.py test_data/test_case_3_invalid.csv
python hospital_analyzer.py test_data/test_case_4_age_groups.csv
```

After each command, use the menu:
- Test 1: choose `1` for department count.
- Test 2: choose `2` for length of stay.
- Test 3: cleaning report appears when the file loads; choose `2` if you also want stay output.
- Test 4: choose `3` for average stay, age groups, and the bar chart.
- Choose `4` to exit each run.

## Expected checks
- Test 1: Cardiology 2, Ortho 1, total 3.
- Test 2: P4 is 0 days; average stay is 0.00 days.
- Test 3: 1 duplicate removed; 1 missing age filled; median age used is 45; 4 records remain.
- Test 4: average stay 3.67 days; age groups 0-40: 1, 41-60: 2, 61+: 0.

## Important assumptions
- Duplicate rows are detected by `Patient_ID`; the first record is kept. This matches the repeated P1 example in the assignment.
- Missing/invalid ages are filled with the median of the valid ages after duplicate removal.
- Length of stay is discharge date minus admission date. Same-day discharge is 0 days.
- Test files are kept separate so the original `patients.csv` remains unchanged.
