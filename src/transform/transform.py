import pandas as pd

from transform.helpers.calculations import profile_calculation, search_calculation
from transform.constants.scores_file import SCORE_FIELDS
from transform.constants.reviews_file import REVIEWS_FILES_FIELDS
from transform.constants.config import SORTING_FIELDS, ROUND_PRECISION


def enrich_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches a DataFrame by adding new columns with required computed.

    Args:
        df (pd.DataFrame): The DataFrame to enrich.
    Returns:
        pd.DataFrame: The enriched DataFrame with new columns.
    """
    df[SCORE_FIELDS["profile_score"]] = df.apply(profile_calculation, axis=1)
    df[SCORE_FIELDS["ratings_score"]] = (
        df.groupby(REVIEWS_FILES_FIELDS["sitter"])[REVIEWS_FILES_FIELDS["rating"]]
        .transform("mean")
        .round(ROUND_PRECISION)
    )
    df[SCORE_FIELDS["num_stays"]] = df.groupby(REVIEWS_FILES_FIELDS["sitter"])[
        REVIEWS_FILES_FIELDS["rating"]
    ].transform("count")
    df[SCORE_FIELDS["search_score"]] = df.apply(search_calculation, axis=1).round(
        ROUND_PRECISION
    )

    return df


def sort_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Sorts the DataFrame based on the search score and sitter name.
    Args:
        df (pd.DataFrame): The DataFrame to sort.
    Returns:
        pd.DataFrame: The sorted DataFrame.
    """
    df.drop_duplicates(
        subset=[REVIEWS_FILES_FIELDS["sitter"]], keep="first", inplace=True
    )
    return df.sort_values(by=SORTING_FIELDS, ascending=[False, True])
