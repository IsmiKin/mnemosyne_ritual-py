import typer
from typing_extensions import Annotated

import utils.logger as logger_factory

import constants.process_phases as PROCESS_PHASES
import extract.extract as extract_logic
import validation.validation as validation_logic
import transform.transform as transform_logic
import persist.persist_disk as persist_disk_logic
import persist.persist_db as persist_db_logic

log = logger_factory.get_logger()


app = typer.Typer()


@app.command()
def version() -> str:
    """Return the version."""
    log.info(f"Version 0.1 !")
    typer.echo(f"Version 0.1 !")


@app.command()
def process_file(
    file_name: str,
    db_persist: Annotated[bool, typer.Option(help="Persist to database.")] = False,
) -> None:
    """
    Process the file stored in the file_name path.

    It will validate the file, extract the data, and calculate scores.

    It will write the results in a csv file in the same directory.

    Args:
        file_name (str): The path to the file to process.
    Returns:
        None
    """
    phases_completed = []
    log.info(f"Processing file: {file_name}")

    # Extract data
    if not extract_logic.file_exists(file_name):
        log.error("File does not exist")
        raise typer.Exit(code=1)

    log.info(f"Extract file: {file_name} successfully")
    phases_completed.append(PROCESS_PHASES.EXTRACT)

    # Validate input file
    is_valid, report = validation_logic.validate_reviews_file(file_name)
    if not is_valid:
        log.error("Validation failed for file: {}".format(file_name))
        log.error(report)
        raise typer.Exit(code=1)

    log.info(f"Validation file: {file_name} successfully")
    phases_completed.append(PROCESS_PHASES.VALIDATE)

    # Transform data
    try:
        dataframe = extract_logic.csv_to_dataframe(file_name)
        enrich_df = transform_logic.enrich_dataframe(dataframe)
        sorted_df = transform_logic.sort_dataframe(enrich_df)
        log.info(f"Transform and sorting file: {file_name} successfully")
        phases_completed.append(PROCESS_PHASES.TRANSFORM)
    except Exception as e:
        log.error(f"Error transforming data: {e}")

    # Persist data
    try:
        ## TODO: Add validation for output file
        persist_disk_logic.persist_dataframe_csv(sorted_df, file_name)
        phases_completed.append(PROCESS_PHASES.PERSIST)
        log.info(
            "File processed successfully. Output saved to {}-output.csv".format(
                file_name
            )
        )
    except Exception as e:
        log.error(f"Error persisting data: {e}")

    if db_persist:
        log.info("Persisting data to database")

        pipeline = persist_db_logic.create_sitter_scores_pipeline(
            file_name, phases_completed
        )

        persist_db_logic.persist_dataframe_db(sorted_df, pipeline.uuid.hex)
        log.info("Data persisted to database successfully")


if __name__ == "__main__":
    app()
