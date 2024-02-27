from datetime import datetime

from pydantic import BaseModel, Field, UUID4, field_validator


# Base model for log items, allow extra fields
class LogItem(BaseModel, extra='allow'):
    # Field(...) makes fields to be required
    service_id: UUID4 = Field(...)
    # Assuming that all audit logs can be connected to a specific user,
    # otherwise make it optional
    customer_id: UUID4 = Field(...)
    event_type: str = Field(...)
    event_timestamp: datetime = Field(...)
    description: str = Field(...)
    # optional fields
    actor_id: UUID4 = None

    @field_validator("service_id", "customer_id", "actor_id")
    def validate_uuids(cls, value):
        if value:
            return str(value)
        return value

    # TODO think of other possible fields, e.g. CorrelationId

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "service_id": "550e8400-e29b-41d4-a716-446655440000",
                "customer_id": "cac22779-bbf7-442b-a609-736d2429d0b3",
                "event_type": "CREATE",
                "event_timestamp": datetime(2011, 11, 4, 0, 0),
                "description": "The new account is created"
            }
        }
