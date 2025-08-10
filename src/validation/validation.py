from frictionless import Schema, describe, validate

import validation.constants.models as models
import validation.constants.config as config


def compose_model_path(model_name: str) -> str:
    return "{}/{}.{}".format(config.MODELS_PATH, model_name, config.MODELS_FORMAT)


def validate_reviews_file(file_name: str) -> bool:
    return validate_file(
        file_name, model_path=compose_model_path(model_name=models.REVIEWS)
    )


def validate_scores_file(file_name: str) -> bool:
    return validate_file(
        file_name, model_path=compose_model_path(model_name=models.SCORES)
    )


def validate_file(file_name: str, model_path: str) -> bool:
    schema = Schema.from_descriptor(model_path)
    file_resource = describe(file_name, format=config.FILE_NAME_FORMAT, schema=schema)
    report = validate(file_resource)

    return report.valid, report.to_summary()
