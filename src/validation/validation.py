from frictionless import Schema, describe, validate

import validation.constants.models as models
import validation.constants.config as config


def compose_model_path(model_name: str) -> str:
    """Compose the path to the validation model file.
    Args:
        model_name (str): The name of the model to compose the path for.
    Returns:
        str: The full path to the model file.
    """
    return "{}/{}.{}".format(config.MODELS_PATH, model_name, config.MODELS_FORMAT)


def validate_file(file_name: str, model_path: str) -> bool:
    """Validate a file against a defined schema.
    Args:
        file_name (str): The path to the file to validate.
        model_path (str): The path to the model schema to validate against.
    Returns:
        bool: True if the file is valid, False otherwise.
    """
    schema = Schema.from_descriptor(model_path)
    file_resource = describe(file_name, format=config.FILE_NAME_FORMAT, schema=schema)
    report = validate(file_resource)

    return report.valid, report.to_summary()


def validate_reviews_file(file_name: str) -> bool:
    """Validate the reviews file against the defined schema. Wrapper for reviews model.
    Args:
        file_name (str): The path to the reviews file to validate.
    Returns:
        bool: True if the file is valid, False otherwise.
    """
    return validate_file(
        file_name, model_path=compose_model_path(model_name=models.REVIEWS)
    )


def validate_scores_file(file_name: str) -> bool:
    """Validate the scores file against the defined schema. Wrapper for scores model.
    Args:
        file_name (str): The path to the scores file to validate.
    Returns:
        bool: True if the file is valid, False otherwise.
    """
    return validate_file(
        file_name, model_path=compose_model_path(model_name=models.SCORES)
    )
