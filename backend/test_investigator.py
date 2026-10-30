import pandas as pd
import json

from services.investigator import investigate_hypothesis


# Load sample dataset
df = pd.read_csv("../sample_data/students.csv")


# Select a hypothesis
hypothesis = {
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


print("DataDetective is investigating...\n")

result = investigate_hypothesis(
    df,
    hypothesis
)

print(json.dumps(result, indent=4))