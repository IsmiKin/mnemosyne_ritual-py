import pandas as pd
from persist.constants.scores import REQUIRED_FIELDS


def persist_dataframe_csv(df: pd.DataFrame, file_name: str) -> None:
    """
    Persists the DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to persist.
        file_name (str): The name of the file to save the DataFrame to.
    Returns:
        None
    """
    file_name_output = "{}-output.csv".format(file_name)
    truncated_df = df[REQUIRED_FIELDS]
    truncated_df.to_csv(file_name_output, index=False)
