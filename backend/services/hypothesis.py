import json
import re

from pydantic import BaseModel, Field, ValidationError
from typing import Literal

from services.nemotron import ask_nemotron


# Define the structure of a hypothesis
class Hypothesis(BaseModel):

    id: int

    hypothesis: str = Field(min_length=10)

    columns: list[str] = Field(min_length=2, max_length=2)

    recommended_test: Literal[
        "pearson_correlation",
        "chi_square",
        "welch_t_test"
    ]

    explanation: str = Field(min_length=10)


# Define the structure of the AI response
class HypothesisResponse(BaseModel):

    hypotheses: list[Hypothesis] = Field(
        min_length=1,
        max_length=3
    )


def generate_hypotheses(dataset_profile):

    # Get the available column names
    column_profiles = dataset_profile["column_profiles"]

    available_columns = list(column_profiles.keys())

    # Create the prompt for Nemotron
    prompt = f"""
You are DataDetective, an expert AI data scientist.

Your task is to generate up to 3 meaningful,
statistically testable hypotheses based on
the dataset profile below.

DATASET PROFILE:
{json.dumps(dataset_profile, indent=2, default=str)}

RULES:

1. Only use columns that actually exist in the dataset.

2. Do not invent data, calculations, p-values,
   correlations, or statistical findings.

3. Every hypothesis must use exactly two columns.

4. Only recommend one of these statistical tests:

   pearson_correlation:
   Use for two numerical variables.

   chi_square:
   Use for two categorical variables.

   welch_t_test:
   Use for one numerical variable and one
   categorical variable with exactly two groups.

5. Avoid identifier columns such as student names,
   customer IDs, or transaction IDs.

6. Generate diverse, meaningful hypotheses.

7. If fewer than three valid hypotheses are possible,
   return fewer than three.

8. Return ONLY valid JSON in this exact format:

{{
  "hypotheses": [
    {{
      "id": 1,
      "hypothesis": "Your hypothesis here",
      "columns": ["Column1", "Column2"],
      "recommended_test": "pearson_correlation",
      "explanation": "Why this test is appropriate"
    }}
  ]
}}

Do not include Markdown code fences or explanations
outside the JSON.
"""

    # Send the prompt to NVIDIA Nemotron
    response = ask_nemotron(prompt)

    # Remove optional Markdown code fences
    cleaned_response = response.strip()

    cleaned_response = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned_response
    )

    cleaned_response = re.sub(
        r"\s*```$",
        "",
        cleaned_response
    )

    # Convert the AI response into Python data
    try:
        parsed_response = json.loads(cleaned_response)

        validated_response = HypothesisResponse.model_validate(
            parsed_response
        )

    except (json.JSONDecodeError, ValidationError) as error:

        raise ValueError(
            f"Nemotron returned an invalid hypothesis response: {error}"
        )

    # Validate column names and statistical test compatibility
    valid_hypotheses = []

    for hypothesis in validated_response.hypotheses:

        column1, column2 = hypothesis.columns

        # Reject nonexistent or duplicate columns
        if (
            column1 not in available_columns
            or column2 not in available_columns
            or column1 == column2
        ):
            continue

        info1 = column_profiles[column1]
        info2 = column_profiles[column2]

        def is_numeric(info):
            return info["data_type"] in [
                "int64",
                "int32",
                "float64",
                "float32"
            ]

        numeric1 = is_numeric(info1)
        numeric2 = is_numeric(info2)

        test = hypothesis.recommended_test

        # Pearson correlation requires two numeric columns
        if test == "pearson_correlation":
            if not (numeric1 and numeric2):
                continue

        # Chi-square requires two categorical columns
        elif test == "chi_square":
            if numeric1 or numeric2:
                continue

        # Welch's t-test requires one numeric column
        # and one categorical column with exactly two groups
        elif test == "welch_t_test":

            if numeric1 == numeric2:
                continue

            categorical_info = info2 if numeric1 else info1

            if categorical_info["unique_values"] != 2:
                continue

        valid_hypotheses.append(
            hypothesis.model_dump()
        )

    return {
        "hypotheses": valid_hypotheses
    }