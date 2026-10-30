import pandas as pd
import json

from services.data_profiler import profile_dataset

# Load student dataset
df = pd.read_csv("../sample_data/students.csv")

# Generate profile
profile = profile_dataset(df)

# Display results
print(json.dumps(profile, indent=4))