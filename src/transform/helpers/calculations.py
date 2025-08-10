import pandas as pd
from statistics import fmean
from string import ascii_letters

from transform.constants.reviews_file import REVIEWS_FILES_FIELDS
from transform.constants.scores_file import SCORE_FIELDS
import transform.constants.config as config


def profile_calculation(row: pd.Series) -> int:
    letters_set = set(ascii_letters)
    unique_letters = set(row[REVIEWS_FILES_FIELDS["sitter"]].lower())
    result = list(filter(lambda char: char in letters_set, unique_letters))

    # NOTE: Question: Why 5? I think without the five it would be better
    return len(result) * config.PROFILE_SCORE_MODIFIER


def search_calculation(row: pd.Series) -> float:
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
