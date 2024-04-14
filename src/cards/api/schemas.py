from typing import Optional, List
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field

from ..core.constants import ID_LENGTH


CardsIdField = Field(
    pattern=r"^[a-zA-Z0-9]{" + rf"{ID_LENGTH}" + r"}$",
    alias="card_id",
    default="aAbBcC10",
)


class CardsStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"


class CardSpecSchema(BaseModel):
    term: Optional[str] = Field(
        max_length=128,
        alias="term",
        default=None,
    )

    description: Optional[str] = Field(
        max_length=512,
        alias="description",
        default=None,
    )

    status: Optional[CardsStatus] = Field(
        alias="status",
        default=None,
    )


class CardsetInfoSpecSchema(BaseModel):
    title: Optional[str] = Field(
        max_length=128,
        alias="title",
        default=None,
    )

    description: Optional[str] = Field(
        max_length=512,
        alias="description",
        default=None,
    )

    status: Optional[CardsStatus] = Field(
        alias="status",
        default=None,
    )


class CardsetSpecSchema(CardsetInfoSpecSchema):
    cards: Optional[List[CardSpecSchema]] = Field(
        alias="cards",
        default=None,
    )


class CardSchema(BaseModel):
    card_id: str
    cardset_id: str
    term: str
    description: str
    created_at: datetime
    modified_at: datetime
    addressed_at: datetime
    status: CardsStatus
    owner_id: str


class CardsSchema(BaseModel):
    cards: List[CardSchema]


class CardsetInfoSchema(BaseModel):
    title: str
    cardset_id: str
    description: str
    created_at: datetime
    modified_at: datetime
    addressed_at: datetime
    status: CardsStatus
    owner_id: str


class CardsetInfosSchema(BaseModel):
    cardsets: List[CardsetInfoSchema]
