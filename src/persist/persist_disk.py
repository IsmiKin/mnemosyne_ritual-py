import os
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
    filename_without_extension = os.path.splitext(file_name)[0]
    file_name_output = "{}-output.csv".format(filename_without_extension)
    truncated_df = df[REQUIRED_FIELDS]
    truncated_df.to_csv(file_name_output, index=False)
