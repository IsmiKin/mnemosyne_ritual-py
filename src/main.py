import typer

import utils.logger as logger_factory

import extract.extract as extract_logic
import validation.validation as validation_logic
import transform.transform as transform_logic
import persist.persist as persist_logic

log = logger_factory.get_logger()


app = typer.Typer()


@app.command()
def process_file(file_name: str):
    """ "
    Process the file stored in the file_name path.

    It will validate the file, extract the data, and calculate scores.

    It will write the results in a csv file in the same directory.

    Args:
        file_name (str): The path to the file to process.
    Returns:
        None
    """
    log.info(f"Processing file: {file_name}")

    # Extract data
    if not extract_logic.file_exists(file_name):
        log.error("File does not exist")
        raise typer.Exit(code=1)

    log.info(f"Extract file: {file_name} successfully")

    # Validate input file
    is_valid, report = validation_logic.validate_reviews_file(file_name)
    if not is_valid:
        log.error("Validation failed for file: {}".format(file_name))
        log.error(report)
        raise typer.Exit(code=1)

    log.info(f"Validation file: {file_name} successfully")

    # Transform data
    dataframe = extract_logic.csv_to_dataframe(file_name)
    enrich_df = transform_logic.enrich_dataframe(dataframe)
    sorted_df = transform_logic.sort_dataframe(enrich_df)

    log.info(f"Transform and sorting file: {file_name} successfully")

    # Persist data
    persist_logic.persist_dataframe_csv(sorted_df, file_name)
    log.info(
        "File processed successfully. Output saved to {}-output.csv".format(file_name)
    )


if __name__ == "__main__":
    app()
