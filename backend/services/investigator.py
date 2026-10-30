from services.statistics import run_statistical_test
from services.interpretation import interpret_results


def investigate_hypothesis(df, hypothesis):

    # STEP 1: Run the statistical test
    statistical_results = run_statistical_test(
        df,
        hypothesis
    )

    # STEP 2: Ask Nemotron to interpret results
    interpretation = interpret_results(
        hypothesis,
        statistical_results
    )

    # STEP 3: Build the evidence trail
    evidence_trail = {
        "hypothesis": hypothesis["hypothesis"],
        "columns": hypothesis["columns"],
        "selected_test": hypothesis["recommended_test"],
        "statistical_results": statistical_results,
        "ai_interpretation": interpretation
    }

    return evidence_trail