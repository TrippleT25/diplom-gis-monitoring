from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.repositories.measurements import (
    create_measurement,
    get_measurements,
)
from app.repositories.monitoring_objects import (
    get_monitoring_object_by_id,
)
from app.routers.auth import get_current_user
from app.schemas import (
    MeasurementCreate,
    MeasurementRead,
)


router = APIRouter(
    prefix="/monitoring-objects",
    tags=["Measurements"],
)


@router.post(
    "/{object_id}/measurements",
    response_model=MeasurementRead,
    status_code=status.HTTP_201_CREATED,
)
def add_measurement(
    object_id: int,
    data: MeasurementCreate,
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

    return create_measurement(
        db=db,
        monitoring_object_id=object_id,
        value=data.value,
    )


@router.get(
    "/{object_id}/measurements",
    response_model=list[MeasurementRead],
)
def list_measurements(
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

    return get_measurements(
        db=db,
        monitoring_object_id=object_id,
    )