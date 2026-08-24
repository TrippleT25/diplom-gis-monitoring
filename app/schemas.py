from pydantic import BaseModel, ConfigDict, Field


class MonitoringObjectCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255,
    )

    latitude: float = Field(
        ge=-90,
        le=90,
    )

    longitude: float = Field(
        ge=-180,
        le=180,
    )


class MonitoringObjectRead(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)