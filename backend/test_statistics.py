import pandas as pd
import json

from services.statistics import run_statistical_test


# Load dataset
df = pd.read_csv("../sample_data/students.csv")


# Hypothesis 1
hypothesis1 = {
    "id": 1,
    "hypothesis": (
        "Students who study more hours achieve "
        "higher exam scores."
    ),
    "columns": [
        "Study_Hours",
        "Exam_Score"
    ],
    "recommended_test": "pearson_correlation"
}


# Hypothesis 2
hypothesis2 = {
    "id": 2,
    "hypothesis": (
        "Students who pass have higher attendance."
    ),
    "columns": [
        "Attendance",
        "Passed"
    ],
    "recommended_test": "welch_t_test"
}


print("\nINVESTIGATION 1")
result1 = run_statistical_test(df, hypothesis1)
print(json.dumps(result1, indent=4))


print("\nINVESTIGATION 2")
result2 = run_statistical_test(df, hypothesis2)
print(json.dumps(result2, indent=4))