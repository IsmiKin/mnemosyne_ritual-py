import os
import pandas as pd


def file_exists(file_path):
    if not os.path.isfile(file_path):
        raise Exception("File does not exists")


def csv_to_dataframe(file_path):
    file_exists(file_path)
    try:
        return pd.read_csv(file_path, sep=",", encoding="utf-8")
    except Exception as error:
        raise Exception("Error reading CSV file: {}".format(error))
