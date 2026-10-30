import pandas as pd

from scipy.stats import (
    pearsonr,
    chi2_contingency,
    ttest_ind
)


# -----------------------------------------
# TOOL 1: PEARSON CORRELATION
# -----------------------------------------

def pearson_correlation(df, column1, column2):

    # Select the columns and remove missing values
    data = df[[column1, column2]].dropna()

    # Make sure both columns contain numbers
    if not all(
        pd.api.types.is_numeric_dtype(data[col])
        for col in [column1, column2]
    ):
        raise ValueError(
            "Pearson correlation requires two numerical columns."
        )

    # Need at least three observations
    if len(data) < 3:
        raise ValueError(
            "Not enough observations for correlation."
        )

    # Reject constant columns
    if (
        data[column1].nunique() < 2
        or data[column2].nunique() < 2
    ):
        raise ValueError(
            "Cannot calculate correlation with constant columns."
        )

    # Calculate correlation and p-value
    correlation, p_value = pearsonr(
        data[column1],
        data[column2]
    )

    return {
        "test": "pearson_correlation",
        "columns": [column1, column2],
        "sample_size": len(data),
        "correlation": float(correlation),
        "p_value": float(p_value)
    }


# -----------------------------------------
# TOOL 2: CHI-SQUARE TEST
# -----------------------------------------

def chi_square_test(df, column1, column2):

    data = df[[column1, column2]].dropna()

    # Build a contingency table
    contingency_table = pd.crosstab(
        data[column1],
        data[column2]
    )

    # Require at least two categories per column
    if (
        contingency_table.shape[0] < 2
        or contingency_table.shape[1] < 2
    ):
        raise ValueError(
            "Chi-square requires at least two categories per variable."
        )

    chi2, p_value, dof, expected = chi2_contingency(
        contingency_table
    )

    # Flag small expected cell counts
    assumptions_warning = None

    if (expected < 5).any():
        assumptions_warning = (
            "Some expected cell counts are below 5. "
            "The chi-square approximation may be unreliable."
        )

    return {
        "test": "chi_square",
        "columns": [column1, column2],
        "sample_size": len(data),
        "chi_square_statistic": float(chi2),
        "p_value": float(p_value),
        "degrees_of_freedom": int(dof),
        "contingency_table": contingency_table.to_dict(),
        "assumptions_warning": assumptions_warning
    }


# -----------------------------------------
# TOOL 3: WELCH'S T-TEST
# -----------------------------------------

def welch_t_test(df, numeric_column, group_column):

    data = df[[numeric_column, group_column]].dropna()

    if not pd.api.types.is_numeric_dtype(
        data[numeric_column]
    ):
        raise ValueError(
            "The measurement column must be numerical."
        )

    # Identify the groups
    groups = data[group_column].unique()

    if len(groups) != 2:
        raise ValueError(
            "Welch's t-test requires exactly two groups."
        )

    group1 = data[
        data[group_column] == groups[0]
    ][numeric_column]

    group2 = data[
        data[group_column] == groups[1]
    ][numeric_column]

    # Each group needs at least two observations
    if len(group1) < 2 or len(group2) < 2:
        raise ValueError(
            "Each group must contain at least two observations."
        )

    # Run Welch's t-test
    statistic, p_value = ttest_ind(
        group1,
        group2,
        equal_var=False
    )

    return {
        "test": "welch_t_test",
        "columns": [numeric_column, group_column],
        "group1": str(groups[0]),
        "group2": str(groups[1]),
        "group1_size": len(group1),
        "group2_size": len(group2),
        "group1_mean": float(group1.mean()),
        "group2_mean": float(group2.mean()),
        "t_statistic": float(statistic),
        "p_value": float(p_value)
    }


# -----------------------------------------
# TOOL ROUTER
# -----------------------------------------

def run_statistical_test(df, hypothesis):

    test = hypothesis["recommended_test"]
    columns = hypothesis["columns"]

    if len(columns) != 2:
        raise ValueError(
            "Exactly two columns are required."
        )

    column1, column2 = columns

    # Validate column names
    if column1 not in df.columns or column2 not in df.columns:
        raise ValueError(
            "Hypothesis references a nonexistent column."
        )

    if column1 == column2:
        raise ValueError(
            "Please select two different columns."
        )

    if test == "pearson_correlation":

        return pearson_correlation(
            df, column1, column2
        )

    elif test == "chi_square":

        return chi_square_test(
            df, column1, column2
        )

    elif test == "welch_t_test":

        # Determine which column is numerical
        numeric_columns = [
            col for col in columns
            if pd.api.types.is_numeric_dtype(df[col])
        ]

        if len(numeric_columns) != 1:
            raise ValueError(
                "Welch's t-test requires one numeric column."
            )

        numeric_column = numeric_columns[0]

        group_column = (
            column2 if numeric_column == column1
            else column1
        )

        return welch_t_test(
            df,
            numeric_column,
            group_column
        )

    else:
        raise ValueError(
            f"Unsupported statistical test: {test}"
        )