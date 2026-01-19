from __future__ import annotations

import json

from auth import AuthManager


def test_create_user_and_authenticate(tmp_path) -> None:
    users_path = tmp_path / "users.json"
    auth = AuthManager(users_path)

    assert auth.create_user("alice", "password123") is True

    stored = json.loads(users_path.read_text(encoding="utf-8"))
    assert stored == [{"username": "alice", "password": "password123"}]

    assert auth.authenticate("alice", "password123") is True
    assert auth.authenticate("alice", "wrong") is False
    assert auth.authenticate("bob", "password123") is False


def test_duplicate_user_rejected(tmp_path) -> None:
    users_path = tmp_path / "users.json"
    auth = AuthManager(users_path)

    assert auth.create_user("alice", "password123") is True
    assert auth.create_user("alice", "password123") is False
