from pydantic import BaseModel, ConfigDict, Field
from pydantic import EmailStr
from datetime import datetime

class MonitoringObjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class MonitoringObjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class MonitoringObjectRead(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

class MeasurementCreate(BaseModel):
    value: float = Field(ge=0)


class MeasurementRead(BaseModel):
    id: int
    monitoring_object_id: int
    value: float
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)

