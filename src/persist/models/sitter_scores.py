from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    UUID,
    Double,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class SitterScores(Base):
    __tablename__ = "sitter_scores"
    __table_args__ = (
        ForeignKeyConstraint(
            ["last_update_pipeline_FK"],
            ["sitter_scores_pipelines.uuid"],
            name="sitter_scores_last_update_pipeline_FK_fkey",
        ),
        PrimaryKeyConstraint("uuid", name="sitter_scores_pkey"),
        Index("sitter_search_score", "search_score"),
    )

    uuid: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid4, server_default=text("gen_random_uuid()")
    )
    sitter: Mapped[str] = mapped_column(Text)
    sitter_email: Mapped[str] = mapped_column(Text)
    profile_score: Mapped[int] = mapped_column(Integer)
    ratings_score: Mapped[Optional[float]] = mapped_column(Double(53))
    search_score: Mapped[Optional[float]] = mapped_column(Double(53))
    last_update_pipeline_FK: Mapped[UUID] = mapped_column(UUID)

    sitter_scores_pipelines: Mapped["SitterScoresPipelines"] = relationship(
        "SitterScoresPipelines", back_populates="sitter_scores"
    )
