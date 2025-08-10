from typing import List
from sqlalchemy import (
    UUID,
    DateTime,
    PrimaryKeyConstraint,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from uuid import uuid4
from .base import Base


class SitterScoresPipelines(Base):
    __tablename__ = "sitter_scores_pipelines"
    __table_args__ = (
        PrimaryKeyConstraint("uuid", name="sitter_scores_pipelines_pkey"),
    )

    uuid: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    filename: Mapped[str] = mapped_column(Text)
    file_time_update: Mapped[datetime.datetime] = mapped_column(DateTime)
    phases_completed: Mapped[str] = mapped_column(Text)

    sitter_scores: Mapped[List["SitterScores"]] = relationship(
        "SitterScores", back_populates="sitter_scores_pipelines"
    )
