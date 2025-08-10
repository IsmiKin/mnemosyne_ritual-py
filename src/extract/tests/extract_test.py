import pytest
import pandas as pd
import pandas.testing as pd_testing
from pathlib import Path


from extract.extract import file_exists, csv_to_dataframe
import extract.constants.config as config


# --- Tests for file_exists ---


def test_file_exists_returns_true_for_existing_file(tmp_path: Path):
    """
    Tests that file_exists returns True when the file is present.
    `tmp_path` is a pytest fixture that provides a temporary directory.
    """
    # Create a dummy file in the temporary directory
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("content")

    assert file_exists(str(p)) is True


def test_file_exists_returns_false_for_non_existing_file():
    """
    Tests that file_exists returns False for a path that does not exist.
    """
    assert file_exists("non_existent_directory/non_existent_file.txt") is False


def test_file_exists_returns_false_for_directory(tmp_path: Path):
    """
    Tests that file_exists returns False when the path is a directory, not a file.
    """
    assert file_exists(str(tmp_path)) is False


# --- Tests for csv_to_dataframe ---


def test_csv_to_dataframe_successfully_reads_csv(tmp_path: Path):
    """
    Tests that a valid CSV file is correctly read into a pandas DataFrame.
    """
    # Create a dummy CSV file
    file_path = tmp_path / "test_data.csv"
    csv_content = "col1,col2\nval1,val2\nval3,val4"
    file_path.write_text(csv_content, encoding=config.ENCODING)

    # Expected DataFrame
    expected_df = pd.DataFrame({"col1": ["val1", "val3"], "col2": ["val2", "val4"]})

    # Execute the function
    result_df = csv_to_dataframe(str(file_path))

    # Assert that the resulting DataFrame is the same as the expected one
    pd_testing.assert_frame_equal(result_df, expected_df)


def test_csv_to_dataframe_raises_exception_for_non_existent_file():
    """
    Tests that the function raises a generic Exception when the file does not exist.
    """
    with pytest.raises(Exception, match="Error reading CSV file"):
        csv_to_dataframe("path/to/non_existent_file.csv")
