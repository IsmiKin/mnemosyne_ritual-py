import pytest
import pandas as pd
from statistics import fmean

from transform.helpers.calculations import profile_calculation, search_calculation
from transform.constants.reviews_file import REVIEWS_FILES_FIELDS
from transform.constants.scores_file import SCORE_FIELDS
import transform.constants.config as config


# --- Tests for profile_calculation ---


@pytest.mark.parametrize(
    "sitter_name, expected_score",
    [
        ("Alex", 20),  # 4 unique letters (a, l, e, x) * 5 = 20
        ("Bob", 10),  # 2 unique letters (b, o) * 5 = 10
        ("Sally", 20),  # 4 unique letters (s, a, l, y) * 5 = 20
        (
            "sitterA@test.com",
            45,
        ),  # 9 unique letters (s,i,t,e,r,a,o,m,c) * 5 = 45
        ("12345", 0),  # 0 unique letters * 5 = 0
        ("", 0),  # 0 unique letters * 5 = 0
    ],
)
def test_profile_calculation(sitter_name, expected_score):
    """
    Tests profile_calculation with various sitter names.
    """
    # Create a sample row (as a pandas Series) to pass to the function
    row = pd.Series({REVIEWS_FILES_FIELDS["sitter"]: sitter_name})
    assert profile_calculation(row) == expected_score


# --- Tests for search_calculation ---


@pytest.mark.parametrize(
    "profile_score, ratings_score, num_stays, expected_search_score",
    [
        # Case 1: ratings_score is 0, should return profile_score
        (25, 0, 5, 25),
        # Case 2: num_stays > NUM_STAYS_BORDER, should return ratings_score
        (25, 4.5, 11, 4.5),
        (25, 3.8, 20, 3.8),
        # Case 3: num_stays <= NUM_STAYS_BORDER, should be a weighted average
        (
            20,
            4.0,
            5,
            12.0,
        ),  # profile_weight=0.5, rating_weight=0.5 -> (20*0.5 + 4*0.5) = 12
        (
            25,
            5.0,
            10,
            5.0,
        ),  # profile_weight=0.0, rating_weight=1.0 -> returns ratings_score
        (
            30,
            3.0,
            1,
            27.3,
        ),  # profile_weight=0.9, rating_weight=0.1 -> fmean([30, 3], weights=[0.9, 0.1]) = 27.3
    ],
)
def test_search_calculation(
    profile_score, ratings_score, num_stays, expected_search_score
):
    """
    Tests search_calculation across its different logic paths.
    """
    # Create a sample row with the necessary fields
    row = pd.Series(
        {
            SCORE_FIELDS["profile_score"]: profile_score,
            SCORE_FIELDS["ratings_score"]: ratings_score,
            SCORE_FIELDS["num_stays"]: num_stays,
        }
    )
    assert search_calculation(row) == pytest.approx(expected_search_score)
