import pandas as pd
import numpy as np


def profile_dataset(df):
    """
    Analyze a pandas DataFrame and return
    a detailed statistical profile.
    """

    # STEP 1: Basic dataset information
    profile = {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_profiles": {},
        "correlations": {},
    }

    # STEP 2: Analyze each column
    for column in df.columns:

        series = df[column]

        column_info = {
            "data_type": str(series.dtype),
            "missing_count": int(series.isnull().sum()),
            "missing_percentage": round(
                series.isnull().mean() * 100, 2
            ),
            "unique_values": int(series.nunique()),
        }

        # STEP 3: Numerical statistics
        if pd.api.types.is_numeric_dtype(series):

            numeric_data = series.dropna()

            if not numeric_data.empty:

                column_info["statistics"] = {
                    "mean": float(numeric_data.mean()),
                    "median": float(numeric_data.median()),
                    "std": (
                        float(numeric_data.std())
                        if len(numeric_data) > 1
                        else None
                    ),
                    "min": float(numeric_data.min()),
                    "max": float(numeric_data.max()),
                }

                # STEP 4: Detect potential outliers
                q1 = numeric_data.quantile(0.25)
                q3 = numeric_data.quantile(0.75)

                iqr = q3 - q1

                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                outliers = numeric_data[
                    (numeric_data < lower_bound)
                    | (numeric_data > upper_bound)
                ]

                column_info["outliers"] = {
                    "count": int(len(outliers)),
                    "percentage": round(
                        len(outliers) / len(numeric_data) * 100,
                        2
                    ),
                }

        # STEP 5: Categorical statistics
        else:

            counts = series.value_counts().head(5)

            column_info["top_values"] = {
                str(key): int(value)
                for key, value in counts.items()
            }

        profile["column_profiles"][column] = column_info

    # STEP 6: Calculate numerical correlations
    numeric_df = df.select_dtypes(include=[np.number])

    # Exclude constant columns
    numeric_df = numeric_df.loc[
        :, numeric_df.nunique() > 1
    ]

    if numeric_df.shape[1] >= 2:

        correlation_matrix = numeric_df.corr()

        for column in correlation_matrix.columns:

            profile["correlations"][column] = {
                other_column: round(float(value), 3)
                for other_column, value
                in correlation_matrix[column].items()
                if pd.notna(value)
            }

    return profile