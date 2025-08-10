import typer
from pprint import pprint
from statistics import fmean

from string import ascii_letters

import utils.logger as logger_factory

import extract.extract as extract_logic
import validation.validation as validation_logic

log = logger_factory.get_logger()


app = typer.Typer()


def profile_calculation(row):
    letters_set = set(ascii_letters)
    unique_letters = set(row["sitter"].lower())
    result = list(filter(lambda char: char in letters_set, unique_letters))

    # Question: Why 5? I think without the five it would be better
    return len(result) * 5


def search_calculation(row):
    # TODO: MOVE TO CONSTANT
    num_stays_border = 10
    num_stays = row["num_stays"]
    profile_score = row["profile_score"]
    ratings_score = row["ratings_score"]
    # TODO: REMOVE PPRINT
    pprint(
        "p-score: {} ; r-score:{} ; stays: {}".format(
            row["profile_score"], row["ratings_score"], num_stays
        )
    )
    if ratings_score is None or ratings_score == 0:
        return profile_score
    elif num_stays > num_stays_border:
        return ratings_score
    else:
        profile_weight = (num_stays_border - num_stays) / 10
        rating_weight = 1 - profile_weight
        weights = [profile_weight, rating_weight]
        return fmean([profile_score, ratings_score], weights=weights)


@app.command()
def process_file(file_name: str):
    log.info(f"Processing file: {file_name}")

    if not extract_logic.file_exists(file_name):
        log.error("File does not exist")
        raise typer.Exit(code=1)

    # Validate input file
    is_valid, report = validation_logic.validate_reviews_file(file_name)
    if not is_valid:
        log.error("Validation failed for file: {}".format(file_name))
        log.error(report)
        raise typer.Exit(code=1)

    # Extract data
    dataframe = extract_logic.csv_to_dataframe(file_name)

    # TODO: Move to sanitizing utils
    dataframe["profile_score"] = dataframe.apply(profile_calculation, axis=1)
    dataframe["ratings_score"] = (
        dataframe.groupby("sitter")["rating"].transform("mean").round(2)
    )
    dataframe["num_stays"] = dataframe.groupby("sitter")["rating"].transform("count")
    dataframe["search_score"] = dataframe.apply(search_calculation, axis=1).round(2)
    dataframe.drop_duplicates(subset=["sitter"], keep="first", inplace=True)
    df_sorted = dataframe.sort_values(
        by=["search_score", "sitter"], ascending=[False, True]
    )

    pprint(
        df_sorted[
            [
                "sitter",
                "profile_score",
                "ratings_score",
                "search_score",
                "num_stays",
            ]
        ].to_string(index=False)
    )
    print("pika")


# @app.command()
# def validate_file(name: str, formal: bool = False):
#     print("pika2")


if __name__ == "__main__":
    app()
