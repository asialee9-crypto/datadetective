import json
from services.nemotron import ask_nemotron


def generate_investigation_report(
    hypothesis,
    statistical_results
):
    """
    Generate an evidence-based investigation report
    using NVIDIA Nemotron.
    """

    prompt = f"""
You are DataDetective, an AI data scientist.

Your job is to interpret statistical evidence
accurately and explain it to beginners.

HYPOTHESIS:
{hypothesis}

STATISTICAL RESULTS:
{json.dumps(statistical_results, indent=2, default=str)}

INSTRUCTIONS:

1. Explain what the statistical test measures.
2. Interpret the actual numerical results.
3. Explain the meaning of the p-value, if available.
4. State whether the evidence supports the hypothesis.
5. Identify limitations of the analysis.
6. Suggest one useful follow-up investigation.

IMPORTANT RULES:

- Never invent statistical values.
- Never claim correlation proves causation.
- Do not claim a hypothesis is proven.
- If evidence is insufficient, say so.
- If a statistical test failed, explain the failure.
- Do not interpret missing results as zero.
- Use clear, beginner-friendly language.

Return a valid JSON object with these fields:

{{
    "summary": "Short explanation",
    "statistical_interpretation": "Detailed explanation",
    "conclusion": "Evidence-based conclusion",
    "limitations": ["Limitation 1", "Limitation 2"],
    "next_investigation": "Suggested follow-up"
}}

Return ONLY valid JSON.
"""

    response = ask_nemotron(prompt)

    # Handle responses that contain Markdown code fences
    cleaned = response.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        cleaned = cleaned.rsplit("```", 1)[0].strip()

    try:
        report = json.loads(cleaned)

        required_fields = [
            "summary",
            "statistical_interpretation",
            "conclusion",
            "limitations",
            "next_investigation"
        ]

        for field in required_fields:
            if field not in report:
                raise ValueError(
                    f"Missing report field: {field}"
                )

        if not isinstance(report["limitations"], list):
            raise ValueError(
                "The limitations field must be a list."
            )

        return report

    except (json.JSONDecodeError, ValueError):
        return {
            "summary": "The AI report could not be parsed.",
            "statistical_interpretation": (
                "The statistical results are available, "
                "but the AI explanation needs to be retried."
            ),
            "conclusion": "No AI conclusion generated.",
            "limitations": [
                "The model did not return a valid report."
            ],
            "next_investigation": (
                "Retry the investigation report."
            )
        }