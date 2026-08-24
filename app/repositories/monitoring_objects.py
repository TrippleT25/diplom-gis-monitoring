from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.monitoring_object import MonitoringObject
from app.schemas import MonitoringObjectCreate


def create_monitoring_object(
    db: Session,
    data: MonitoringObjectCreate,
) -> MonitoringObject:
    monitoring_object = MonitoringObject(
        name=data.name,
        latitude=data.latitude,
        longitude=data.longitude,
    )

    db.add(monitoring_object)
    db.commit()
    db.refresh(monitoring_object)

    return monitoring_object


def get_monitoring_objects(
    db: Session,
) -> list[MonitoringObject]:
    statement = select(MonitoringObject)

    return list(db.scalars(statement).all())


def get_monitoring_object_by_id(
    db: Session,
    object_id: int,
) -> MonitoringObject | None:
    return db.get(MonitoringObject, object_id)