from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.monitoring_object import MonitoringObject
from app.schemas import MonitoringObjectCreate, MonitoringObjectRead


router = APIRouter(
    prefix="/monitoring-objects",
    tags=["Monitoring Objects"],
)


@router.post(
    "",
    response_model=MonitoringObjectRead,
    status_code=201,
)
def create_monitoring_object(
    data: MonitoringObjectCreate,
    db: Session = Depends(get_db),
):
    monitoring_object = MonitoringObject(
        name=data.name,
        latitude=data.latitude,
        longitude=data.longitude,
    )

    db.add(monitoring_object)
    db.commit()
    db.refresh(monitoring_object)

    return monitoring_object


@router.get(
    "",
    response_model=list[MonitoringObjectRead],
)
def get_monitoring_objects(
    db: Session = Depends(get_db),
):
    statement = select(MonitoringObject)

    return db.scalars(statement).all()