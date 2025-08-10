import os
import pandas as pd

import extract.constants.config as config


def file_exists(file_path: str) -> bool:
    """Check if the file exists at the given path.
    Args:
        file_path (str): The path to the file.
    Returns:
        bool: True if the file exists, False otherwise."""
    return os.path.isfile(file_path)


def csv_to_dataframe(file_path: str) -> pd.DataFrame:
    """Read a CSV file and return a DataFrame.
    Args:
        file_path (str): The path to the CSV file.
    Returns:
        pd.DataFrame: The DataFrame containing the CSV data.
    Raises:
        Exception: If there is an error reading the CSV file."""
    try:
        return pd.read_csv(file_path, sep=config.SEPARATOR, encoding=config.ENCODING)
    except Exception as error:
        raise Exception("Error reading CSV file")
