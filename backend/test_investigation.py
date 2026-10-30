from services.investigation import generate_investigation_report


hypothesis = (
    "Students who study more hours achieve "
    "higher exam scores."
)

# Example statistical results for testing
statistical_results = {
    "test": "pearson_correlation",
    "columns": [
        "Study_Hours",
        "Exam_Score"
    ],
    "correlation_coefficient": 0.82,
    "p_value": 0.003,
    "sample_size": 30
}


report = generate_investigation_report(
    hypothesis,
    statistical_results
)


print("\nDATADETECTIVE INVESTIGATION REPORT\n")

for key, value in report.items():
    print(f"\n{key.upper()}:")
    print(value)