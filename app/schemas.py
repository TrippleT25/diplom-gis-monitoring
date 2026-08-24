from pydantic import BaseModel, ConfigDict


class MonitoringObjectCreate(BaseModel):
    name: str
    latitude: float
    longitude: float


class MonitoringObjectRead(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)