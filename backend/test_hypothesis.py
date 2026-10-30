import pandas as pd
import json

from services.data_profiler import profile_dataset
from services.hypothesis import generate_hypotheses


# STEP 1: Load the sample dataset
df = pd.read_csv("../sample_data/students.csv")


# STEP 2: Generate the statistical profile
profile = profile_dataset(df)


# STEP 3: Ask Nemotron to generate hypotheses
print("Generating AI hypotheses...")

result = generate_hypotheses(profile)


# STEP 4: Display the results
print("\nDataDetective Hypotheses:\n")

print(json.dumps(result, indent=4))