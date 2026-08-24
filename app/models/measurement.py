from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(primary_key=True)

    monitoring_object_id: Mapped[int] = mapped_column(
        ForeignKey("monitoring_objects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    monitoring_object = relationship(
        "MonitoringObject",
        back_populates="measurements",
    )