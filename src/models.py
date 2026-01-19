from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Priority(Enum):
    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"


class Status(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class TodoItem:
    id: str
    title: str
    details: str
    priority: Priority
    status: Status
    owner: str
    created_at: str
    updated_at: str
