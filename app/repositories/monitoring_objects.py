from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.monitoring_object import MonitoringObject
from app.schemas import MonitoringObjectCreate, MonitoringObjectUpdate


def create_monitoring_object(
    db: Session,
    data: MonitoringObjectCreate,
    owner_id: int,
) -> MonitoringObject:
    monitoring_object = MonitoringObject(
        name=data.name,
        latitude=data.latitude,
        longitude=data.longitude,
        owner_id=owner_id,
    )

    db.add(monitoring_object)
    db.commit()
    db.refresh(monitoring_object)

    return monitoring_object


def get_monitoring_objects(
    db: Session,
    owner_id: int,
) -> list[MonitoringObject]:
    statement = select(MonitoringObject).where(
        MonitoringObject.owner_id == owner_id
    )

    return list(db.scalars(statement).all())


def get_monitoring_object_by_id(
    db: Session,
    object_id: int,
    owner_id: int,
) -> MonitoringObject | None:
    statement = select(MonitoringObject).where(
        MonitoringObject.id == object_id,
        MonitoringObject.owner_id == owner_id,
    )

    return db.scalar(statement)


def update_monitoring_object(
    db: Session,
    monitoring_object: MonitoringObject,
    data: MonitoringObjectUpdate,
) -> MonitoringObject:
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(monitoring_object, field, value)

    db.commit()
    db.refresh(monitoring_object)

    return monitoring_object


def delete_monitoring_object(
    db: Session,
    monitoring_object: MonitoringObject,
) -> None:
    db.delete(monitoring_object)
    db.commit()