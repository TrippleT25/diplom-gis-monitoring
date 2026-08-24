from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.monitoring_objects import (
    create_monitoring_object,
    get_monitoring_object_by_id,
    get_monitoring_objects,
)
from app.schemas import MonitoringObjectCreate, MonitoringObjectRead

from app.repositories.monitoring_objects import (
    create_monitoring_object,
    delete_monitoring_object,
    get_monitoring_object_by_id,
    get_monitoring_objects,
    update_monitoring_object,
)

from app.schemas import (
    MonitoringObjectCreate,
    MonitoringObjectRead,
    MonitoringObjectUpdate,
)


router = APIRouter(
    prefix="/monitoring-objects",
    tags=["Monitoring Objects"],
)

from app.models.user import User
from app.routers.auth import get_current_user

@router.post(
    "",
    response_model=MonitoringObjectRead,
    status_code=status.HTTP_201_CREATED,
)
def create_object(
    data: MonitoringObjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_monitoring_object(
        db=db,
        data=data,
        owner_id=current_user.id,
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
    current_user: User = Depends(get_current_user),
):
    return get_monitoring_objects(
        db=db,
        owner_id=current_user.id,
    )

@router.get(
    "/{object_id}",
    response_model=MonitoringObjectRead,
)
def get_object(
    object_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    monitoring_object = get_monitoring_object_by_id(
        db=db,
        object_id=object_id,
        owner_id=current_user.id,
    )

    if monitoring_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring object not found",
        )

    return monitoring_object

@router.patch(
    "/{object_id}",
    response_model=MonitoringObjectRead,
)
def update_object(
    object_id: int,
    data: MonitoringObjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    monitoring_object = get_monitoring_object_by_id(
        db=db,
        object_id=object_id,
        owner_id=current_user.id,
    )

    if monitoring_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring object not found",
        )

    return update_monitoring_object(
        db=db,
        monitoring_object=monitoring_object,
        data=data,
    )

@router.delete(
    "/{object_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_object(
    object_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    monitoring_object = get_monitoring_object_by_id(
        db=db,
        object_id=object_id,
        owner_id=current_user.id,
    )

    if monitoring_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring object not found",
        )

    delete_monitoring_object(
        db=db,
        monitoring_object=monitoring_object,
    )