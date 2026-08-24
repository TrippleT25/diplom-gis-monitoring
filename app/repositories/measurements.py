from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.measurement import Measurement


def create_measurement(
    db: Session,
    monitoring_object_id: int,
    value: float,
) -> Measurement:
    measurement = Measurement(
        monitoring_object_id=monitoring_object_id,
        value=value,
    )

    db.add(measurement)
    db.commit()
    db.refresh(measurement)

    return measurement


def get_measurements(
    db: Session,
    monitoring_object_id: int,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[Measurement]:
    statement = select(Measurement).where(
        Measurement.monitoring_object_id == monitoring_object_id
    )

    if date_from is not None:
        statement = statement.where(
            Measurement.recorded_at >= date_from
        )

    if date_to is not None:
        statement = statement.where(
            Measurement.recorded_at <= date_to
        )

    statement = statement.order_by(
        Measurement.recorded_at.desc()
    )

    return list(db.scalars(statement).all())


def get_measurement_statistics(
    db: Session,
    monitoring_object_id: int,
):
    statement = select(
        func.count(Measurement.id),
        func.min(Measurement.value),
        func.max(Measurement.value),
        func.avg(Measurement.value),
    ).where(
        Measurement.monitoring_object_id == monitoring_object_id
    )

    return db.execute(statement).one()