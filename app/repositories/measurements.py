from sqlalchemy import select
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
) -> list[Measurement]:
    statement = (
        select(Measurement)
        .where(
            Measurement.monitoring_object_id
            == monitoring_object_id
        )
        .order_by(Measurement.recorded_at.desc())
    )

    return list(db.scalars(statement).all())