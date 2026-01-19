from __future__ import annotations

from models import Priority, Status, TodoItem


def test_todo_item_fields() -> None:
    item = TodoItem(
        id="123",
        title="Title",
        details="Details",
        priority=Priority.HIGH,
        status=Status.PENDING,
        owner="alice",
        created_at="2024-01-01T00:00:00+00:00",
        updated_at="2024-01-01T00:00:00+00:00",
    )

    assert item.id == "123"
    assert item.title == "Title"
    assert item.details == "Details"
    assert item.priority is Priority.HIGH
    assert item.status is Status.PENDING
    assert item.owner == "alice"
