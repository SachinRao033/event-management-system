from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


RegistrationStatus = Literal[
    "registered",
    "cancelled",
    "attended",
]


class RegistrationBase(BaseModel):
    event_id: int = Field(gt=0)


class RegistrationCreate(RegistrationBase):
    pass


class RegistrationUpdate(BaseModel):
    status: RegistrationStatus


class RegistrationResponse(RegistrationBase):
    id: int
    user_id: int
    status: RegistrationStatus
    registration_date: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)