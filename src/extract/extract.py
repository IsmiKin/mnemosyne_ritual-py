import os
import pandas as pd

import extract.constants.config as config


def file_exists(file_path: str) -> bool:
    return os.path.isfile(file_path)


def csv_to_dataframe(file_path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path, sep=config.SEPARATOR, encoding=config.ENCODING)
    except Exception as error:
        raise Exception("Error reading CSV file: {}".format(error))
