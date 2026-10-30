import json

from services.nemotron import ask_nemotron


def interpret_results(hypothesis, statistical_results):

    prompt = f"""
You are DataDetective, an AI data science investigator.

A statistical investigation has been completed.

ORIGINAL HYPOTHESIS:
{hypothesis["hypothesis"]}

STATISTICAL RESULTS:
{json.dumps(statistical_results, indent=2)}

Explain the findings in clear, beginner-friendly language.

Your response must include:

1. What was investigated.
2. Which statistical test was used.
3. What the numerical results mean.
4. Whether the evidence supports the hypothesis.
5. Important limitations.

RULES:

- Only use the statistical results provided.
- Never invent additional calculations or findings.
- Do not claim correlation proves causation.
- Explain that statistical significance does not
  necessarily mean practical importance.
- If assumptions are questionable, explain that
  the conclusion may be unreliable.
- If the hypothesis specifies a direction, check
  whether the observed results match it.
- If the sample is small, mention that limitation.
"""

    return ask_nemotron(prompt)