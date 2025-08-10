import pandas as pd
from statistics import fmean
from string import ascii_letters

from transform.constants.reviews_file import REVIEWS_FILES_FIELDS
from transform.constants.scores_file import SCORE_FIELDS
import transform.constants.config as config


def profile_calculation(row: pd.Series) -> int:
    """Calculate the profile score based on the number of unique letters in the sitter's name.
    The score is calculated by counting the unique letters in the sitter's name and multiplying
    by a predefined modifier.
    Args:
        row (pd.Series): A row of the DataFrame containing the sitter's name.
    Returns:
        int: The calculated profile score.
    """

    letters_set = set(ascii_letters)
    sitter_name = set(row[REVIEWS_FILES_FIELDS["sitter"]].lower())
    unique_letters = sitter_name.intersection(letters_set)

    # NOTE: Question: Why 5? I think without the five it would be better
    return len(unique_letters) * config.PROFILE_SCORE_MODIFIER


def search_calculation(row: pd.Series) -> float:
    """Calculate the search score based on the ratings score and profile score.

    The weight of the profile score is increased for sitters with fewer stays,
    while the weight of the ratings score is increased for sitters with more stays.

    Args:
        row (pd.Series): A row of the DataFrame containing the necessary fields.
    Returns:
        float: The calculated search score."""

    num_stays = row[SCORE_FIELDS["num_stays"]]
    profile_score = row[SCORE_FIELDS["profile_score"]]
    ratings_score = row[SCORE_FIELDS["ratings_score"]]

    if ratings_score is None or ratings_score == 0:
        return profile_score
    elif num_stays > config.NUM_STAYS_BORDER:
        return ratings_score
    else:
        profile_weight = (config.NUM_STAYS_BORDER - num_stays) / 10
        rating_weight = 1 - profile_weight
        weights = [profile_weight, rating_weight]
        return fmean([profile_score, ratings_score], weights=weights)
