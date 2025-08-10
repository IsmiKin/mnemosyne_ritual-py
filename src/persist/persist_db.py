import pandas as pd
from datetime import datetime
import uuid

from .models import SitterScoresPipelines, session


def create_sitter_scores_pipeline(
    filename: str, phases_completed: list[str]
) -> SitterScoresPipelines:
    """Create a new SitterScoresPipelines entry."""
    new_pipeline = SitterScoresPipelines(
        filename=filename,
        file_time_update=datetime.now(),
        phases_completed=",".join(phases_completed),
    )
    session.add(new_pipeline)
    session.commit()
    return new_pipeline


def persist_dataframe_db(dataframe: pd.DataFrame, pipeline_uuid: str) -> None:
    """Persist the DataFrame to the database."""
    table_fields = [
        "sitter",
        "profile_score",
        "ratings_score",
        "search_score",
    ]
    cropped_df = pd.DataFrame(dataframe, columns=table_fields)
    cropped_df["last_update_pipeline_FK"] = pipeline_uuid
    cropped_df["uuid"] = cropped_df.apply(lambda _: uuid.uuid4(), axis=1)
    cropped_df.to_sql(
        "sitter_scores", con=session.bind, if_exists="append", index=False
    )
    session.commit()
