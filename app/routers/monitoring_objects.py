from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.monitoring_objects import (
    create_monitoring_object,
    get_monitoring_object_by_id,
    get_monitoring_objects,
)
from app.schemas import MonitoringObjectCreate, MonitoringObjectRead


router = APIRouter(
    prefix="/monitoring-objects",
    tags=["Monitoring Objects"],
)


@router.post(
    "",
    response_model=MonitoringObjectRead,
    status_code=status.HTTP_201_CREATED,
)
def create_object(
    data: MonitoringObjectCreate,
    db: Session = Depends(get_db),
):
    return create_monitoring_object(
        db=db,
        data=data,
    )


@router.get(
    "",
    response_model=list[MonitoringObjectRead],
)
def get_objects(
    db: Session = Depends(get_db),
):
    return get_monitoring_objects(db)


@router.get(
    "/{object_id}",
    response_model=MonitoringObjectRead,
)
def get_object(
    object_id: int,
    db: Session = Depends(get_db),
):
    monitoring_object = get_monitoring_object_by_id(
        db=db,
        object_id=object_id,
    )

    if monitoring_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring object not found",
        )

    return monitoring_object