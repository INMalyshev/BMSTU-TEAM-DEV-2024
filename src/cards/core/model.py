from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class CardsStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"


@dataclass
class Card:
    id: str
    term: str
    description: str
    created_at: datetime
    modified_at: datetime
    addressed_at: datetime
    status: CardsStatus
    owner_id: str


@dataclass
class CardSpec:
    term: Optional[str]
    description: Optional[str]
    status: Optional[CardsStatus]


@dataclass
class CardsetInfo:
    title: str
    id: str
    description: str
    created_at: datetime
    modified_at: datetime
    addressed_at: datetime
    status: CardsStatus
    owner_id: str


@dataclass
class CardsetInfoSpec:
    title: Optional[str]
    description: Optional[str]
    status: Optional[CardsStatus]


@dataclass
class Cardset(CardsetInfo):
    cards: List[Card]


@dataclass
class CardsetSpec(CardsetInfoSpec):
    cards: Optional[List[CardSpec]]
