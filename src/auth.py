from __future__ import annotations

import json
from pathlib import Path


class AuthManager:
    """Manage user signup and authentication using a JSON file."""

    def __init__(self, users_path: Path) -> None:
        self._users_path = users_path

    def _load_users(self) -> list[dict[str, str]]:
        if not self._users_path.exists():
            return []
        with self._users_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, list):
            return [entry for entry in data if isinstance(entry, dict)]
        return []

    def _save_users(self, users: list[dict[str, str]]) -> None:
        with self._users_path.open("w", encoding="utf-8") as handle:
            json.dump(users, handle, indent=2)

    def create_user(self, username: str, password: str) -> bool:
        """Create a new user. Returns False if the username already exists."""
        users = self._load_users()
        if any(user.get("username") == username for user in users):
            return False
        users.append({"username": username, "password": password})
        self._save_users(users)
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Return True if the username and password match a stored user."""
        users = self._load_users()
        return any(
            user.get("username") == username and user.get("password") == password
            for user in users
        )
