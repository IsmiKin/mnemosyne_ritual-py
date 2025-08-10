import pytest
import pandas as pd
import pandas.testing as pd_testing

from transform.transform import enrich_dataframe, sort_dataframe
from transform.constants.scores_file import SCORE_FIELDS
from transform.constants.reviews_file import REVIEWS_FILES_FIELDS
from transform.constants.config import SORTING_FIELDS, ROUND_PRECISION


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """
    Pytest fixture to provide a sample DataFrame for testing.
    This runs once per test function that requests it.
    """
    return pd.DataFrame(
        {
            "sitter": [
                "sitterA@test.com",
                "sitterB@test.com",
                "sitterA@test.com",
                "sitterC@test.com",
                "sitterB@test.com",
            ],
            "rating": [5, 4, 4, 5, 3],
            # Add other columns required by the original functions
            "sitter_image": ["img_A", "img_B", "img_A", "img_C", "img_B"],
            "sitter_phone_number": ["1", "2", "1", "3", "2"],
            "sitter_name": ["Alex", "Bob", "Alex", "Charlie", "Bob"],
        }
    )


def test_enrich_dataframe(sample_dataframe: pd.DataFrame, monkeypatch):
    """
    Tests that the enrich_dataframe function correctly adds all computed columns.
    Uses pytest's monkeypatch fixture to mock helper functions.
    """
    # --- Mocking ---
    # We mock the helper functions to isolate the logic of `enrich_dataframe`.
    # This ensures we are only testing the enrichment process itself.
    mock_profile_values = [10, 20, 10, 30, 20]
    mock_search_values = [9.8, 8.7, 9.8, 7.6, 8.7]

    # Create iterators for the side effects
    profile_iter = iter(mock_profile_values)
    search_iter = iter(mock_search_values)

    # Use monkeypatch to replace the functions during this test
    monkeypatch.setattr(
        "transform.transform.profile_calculation", lambda row: next(profile_iter)
    )
    monkeypatch.setattr(
        "transform.transform.search_calculation", lambda row: next(search_iter)
    )

    # --- Execution ---
    enriched_df = enrich_dataframe(sample_dataframe.copy())

    # --- Assertions ---
    # 1. Check if all new columns are present
    assert SCORE_FIELDS["profile_score"] in enriched_df.columns
    assert SCORE_FIELDS["ratings_score"] in enriched_df.columns
    assert SCORE_FIELDS["num_stays"] in enriched_df.columns
    assert SCORE_FIELDS["search_score"] in enriched_df.columns

    # 2. Check the values of the new columns
    # These values are calculated directly within `enrich_dataframe`
    expected_ratings_score = pd.Series([4.5, 3.5, 4.5, 5.0, 3.5], name="ratings_score")
    expected_num_stays = pd.Series([2, 2, 2, 1, 2], name="num_stays")

    # These values should come from our mocked functions
    expected_profile_score = pd.Series(mock_profile_values, name="profile_score")
    expected_search_score = pd.Series(mock_search_values, name="search_score")

    pd_testing.assert_series_equal(
        enriched_df[SCORE_FIELDS["ratings_score"]],
        expected_ratings_score,
        check_names=False,
    )
    pd_testing.assert_series_equal(
        enriched_df[SCORE_FIELDS["num_stays"]], expected_num_stays, check_names=False
    )
    pd_testing.assert_series_equal(
        enriched_df[SCORE_FIELDS["profile_score"]],
        expected_profile_score,
        check_names=False,
    )
    pd_testing.assert_series_equal(
        enriched_df[SCORE_FIELDS["search_score"]],
        expected_search_score.round(ROUND_PRECISION),  # The function rounds the output
        check_names=False,
    )


def test_sort_dataframe():
    """
    Tests that the sort_dataframe function correctly sorts the DataFrame
    and removes duplicates.
    """
    # --- Setup ---
    # Create a DataFrame that is unsorted and has duplicates
    test_data = {
        "sitter": [
            "sitterC@test.com",
            "sitterB@test.com",
            "sitterC@test.com",  # Duplicate
            "sitterA@test.com",
        ],
        "search_score": [8.5, 9.5, 8.5, 9.5],
        "other_data": [1, 2, 3, 4],
    }
    df_to_sort = pd.DataFrame(test_data)

    # --- Execution ---
    sorted_df = sort_dataframe(df_to_sort.copy())

    # --- Assertions ---
    # Based on SORTING_FIELDS = ["search_score", "sitter"] and ascending=[False, True]
    # 1. sitterA (score 9.5)
    # 2. sitterB (score 9.5)
    # 3. sitterC (score 8.5, first occurrence kept)
    expected_data = {
        "sitter": ["sitterA@test.com", "sitterB@test.com", "sitterC@test.com"],
        "search_score": [9.5, 9.5, 8.5],
        "other_data": [4, 2, 1],
    }
    expected_df = pd.DataFrame(expected_data)

    # `sort_dataframe` modifies inplace and then sorts. We compare the final states.
    # Resetting index is crucial for a correct comparison.
    pd_testing.assert_frame_equal(
        sorted_df.reset_index(drop=True), expected_df.reset_index(drop=True)
    )
