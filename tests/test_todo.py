from __future__ import annotations

import json

from models import Priority, Status
from todo import TodoManager


def test_add_and_list_items(tmp_path) -> None:
    todos_path = tmp_path / "todos.json"
    manager = TodoManager(todos_path)

    item = manager.add_item(
        owner="alice",
        title="Buy milk",
        details="2 liters",
        priority=Priority.HIGH,
    )

    assert item.owner == "alice"
    assert item.title == "Buy milk"
    assert item.details == "2 liters"
    assert item.priority is Priority.HIGH
    assert item.status is Status.PENDING
    assert item.created_at == item.updated_at
    assert item.id

    items = manager.list_items("alice")
    assert len(items) == 1
    assert items[0].id == item.id

    assert manager.list_items("bob") == []

    stored = json.loads(todos_path.read_text(encoding="utf-8"))
    assert stored[0]["priority"] == "HIGH"
    assert stored[0]["status"] == "PENDING"


def test_get_and_update_item(tmp_path, monkeypatch) -> None:
    todos_path = tmp_path / "todos.json"
    manager = TodoManager(todos_path)

    item = manager.add_item(
        owner="alice",
        title="Initial",
        details="Details",
        priority=Priority.MID,
    )

    fetched = manager.get_item(item.id, "alice")
    assert fetched is not None
    assert fetched.title == "Initial"

    monkeypatch.setattr(manager, "_now_iso", lambda: "2024-01-01T00:00:00+00:00")

    updated = manager.update_item(
        item.id,
        "alice",
        {
            "title": "Updated",
            "details": "Updated details",
            "priority": Priority.LOW,
            "status": Status.COMPLETED,
        },
    )

    assert updated is not None
    assert updated.title == "Updated"
    assert updated.details == "Updated details"
    assert updated.priority is Priority.LOW
    assert updated.status is Status.COMPLETED
    assert updated.updated_at == "2024-01-01T00:00:00+00:00"

    missing = manager.update_item("missing", "alice", {"title": "X"})
    assert missing is None


def test_mark_completed(tmp_path) -> None:
    todos_path = tmp_path / "todos.json"
    manager = TodoManager(todos_path)

    item = manager.add_item(
        owner="alice",
        title="Complete me",
        details="Details",
        priority=Priority.MID,
    )

    completed = manager.mark_completed(item.id, "alice")
    assert completed is not None
    assert completed.status is Status.COMPLETED

    not_found = manager.mark_completed("missing", "alice")
    assert not_found is None
