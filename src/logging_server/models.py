from datetime import datetime
from typing import Dict, Union

from pydantic import BaseModel, Field, UUID4, field_serializer, model_serializer


class LogItem(BaseModel):
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
    extra_fields: Union[Dict[str, str], None] = None

    @model_serializer()
    def serialize_model(self):
        partial_res = {'service_id': self.service_id,
                       'customer_id': self.customer_id,
                       'event_type': self.event_type,
                       'event_timestamp': self.event_timestamp,
                       'description': self.description,
                       'actor_id': self.actor_id
                       }
        if self.extra_fields is not None:
            return {**partial_res, **self.extra_fields}
        return partial_res

    # TODO think of other possible fields

    class Config:
        schema_extra = {
            "example": {
                "service_id": "550e8400-e29b-41d4-a716-446655440000",
                "customer_id": "cac22779-bbf7-442b-a609-736d2429d0b3",
                "event_type": "CREATION",
                "event_timestamp": datetime(2011, 11, 4, 0, 0),
                "description": "The new account is created"
            }
        }
