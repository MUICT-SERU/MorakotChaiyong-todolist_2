from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from models import Priority, Status, TodoItem


class TodoManager:
    """Manage to-do items stored in a JSON file."""

    def __init__(self, todos_path: Path) -> None:
        self._todos_path = todos_path

    def _load_items(self) -> list[dict[str, Any]]:
        if not self._todos_path.exists():
            return []
        with self._todos_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, list):
            return [entry for entry in data if isinstance(entry, dict)]
        return []

    def _save_items(self, items: list[dict[str, Any]]) -> None:
        with self._todos_path.open("w", encoding="utf-8") as handle:
            json.dump(items, handle, indent=2)

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _dict_to_item(self, data: dict[str, Any]) -> TodoItem:
        return TodoItem(
            id=str(data.get("id", "")),
            title=str(data.get("title", "")),
            details=str(data.get("details", "")),
            priority=Priority(data.get("priority", Priority.MID.value)),
            status=Status(data.get("status", Status.PENDING.value)),
            owner=str(data.get("owner", "")),
            created_at=str(data.get("created_at", "")),
            updated_at=str(data.get("updated_at", "")),
        )

    def _item_to_dict(self, item: TodoItem) -> dict[str, Any]:
        data = asdict(item)
        data["priority"] = item.priority.value
        data["status"] = item.status.value
        return data

    def add_item(
        self, owner: str, title: str, details: str, priority: Priority
    ) -> TodoItem:
        items = self._load_items()
        now = self._now_iso()
        item = TodoItem(
            id=str(uuid4()),
            title=title,
            details=details,
            priority=priority,
            status=Status.PENDING,
            owner=owner,
            created_at=now,
            updated_at=now,
        )
        items.append(self._item_to_dict(item))
        self._save_items(items)
        return item

    def list_items(self, owner: str) -> list[TodoItem]:
        items = self._load_items()
        owner_items = [item for item in items if item.get("owner") == owner]
        return [self._dict_to_item(item) for item in owner_items]

    def get_item(self, item_id: str, owner: str) -> TodoItem | None:
        items = self._load_items()
        for item in items:
            if item.get("id") == item_id and item.get("owner") == owner:
                return self._dict_to_item(item)
        return None

    def update_item(
        self, item_id: str, owner: str, updates: dict[str, Any]
    ) -> TodoItem | None:
        items = self._load_items()
        for index, item in enumerate(items):
            if item.get("id") != item_id or item.get("owner") != owner:
                continue

            updated = dict(item)
            if "title" in updates:
                updated["title"] = updates["title"]
            if "details" in updates:
                updated["details"] = updates["details"]
            if "priority" in updates:
                updated["priority"] = updates["priority"].value
            if "status" in updates:
                updated["status"] = updates["status"].value
            updated["updated_at"] = self._now_iso()

            items[index] = updated
            self._save_items(items)
            return self._dict_to_item(updated)
        return None

    def mark_completed(self, item_id: str, owner: str) -> TodoItem | None:
        return self.update_item(item_id, owner, {"status": Status.COMPLETED})
