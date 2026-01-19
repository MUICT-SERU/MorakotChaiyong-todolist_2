from __future__ import annotations

from pathlib import Path
from typing import Callable

from auth import AuthManager
from models import Priority, Status, TodoItem
from todo import TodoManager


def prompt_prelogin_choice() -> str:
    print("\n=== To-Do CLI ===")
    print("[1] Login")
    print("[2] Sign Up")
    print("[3] Exit")
    return input("Select an option: ").strip()


def prompt_logged_in_choice(username: str) -> str:
    print(f"\n=== To-Do CLI ({username}) ===")
    print("[1] Create to-do item")
    print("[2] Edit to-do item")
    print("[3] View all to-do items")
    print("[4] View to-do item details")
    print("[5] Mark to-do item as completed")
    print("[6] Logout")
    print("[7] Exit")
    return input("Select an option: ").strip()


def prompt_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Value cannot be empty.")


def prompt_optional(prompt: str) -> str:
    return input(prompt).strip()


def parse_priority(value: str) -> Priority | None:
    normalized = value.strip().upper()
    if not normalized:
        return None
    try:
        return Priority[normalized]
    except KeyError:
        return None


def parse_status(value: str) -> Status | None:
    normalized = value.strip().upper()
    if not normalized:
        return None
    try:
        return Status[normalized]
    except KeyError:
        return None


def prompt_priority(prompt: str, allow_blank: bool = False) -> Priority | None:
    while True:
        raw = input(prompt).strip()
        if allow_blank and not raw:
            return None
        parsed = parse_priority(raw)
        if parsed is not None:
            return parsed
        print("Invalid priority. Use HIGH, MID, or LOW.")


def prompt_status(prompt: str, allow_blank: bool = False) -> Status | None:
    while True:
        raw = input(prompt).strip()
        if allow_blank and not raw:
            return None
        parsed = parse_status(raw)
        if parsed is not None:
            return parsed
        print("Invalid status. Use PENDING or COMPLETED.")


def handle_signup(auth_manager: AuthManager) -> None:
    print("\n=== Sign Up ===")
    username = prompt_non_empty("Username: ")
    password = prompt_non_empty("Password: ")
    if auth_manager.create_user(username, password):
        print("Account created. You can now log in.")
    else:
        print("Username already exists.")


def handle_login(auth_manager: AuthManager) -> str | None:
    print("\n=== Login ===")
    username = prompt_non_empty("Username: ")
    password = prompt_non_empty("Password: ")
    if auth_manager.authenticate(username, password):
        print("Login successful.")
        return username
    print("Invalid username or password.")
    return None


def show_item_summary(item: TodoItem) -> None:
    print(
        f"- {item.id} | {item.title} | {item.priority.value} | "
        f"{item.status.value} | updated {item.updated_at}"
    )


def show_item_details(item: TodoItem) -> None:
    print("\n=== To-Do Details ===")
    print(f"ID: {item.id}")
    print(f"Title: {item.title}")
    print(f"Details: {item.details}")
    print(f"Priority: {item.priority.value}")
    print(f"Status: {item.status.value}")
    print(f"Owner: {item.owner}")
    print(f"Created: {item.created_at}")
    print(f"Updated: {item.updated_at}")


def handle_create(todo_manager: TodoManager, username: str) -> None:
    print("\n=== Create To-Do ===")
    title = prompt_non_empty("Title: ")
    details = prompt_non_empty("Details: ")
    priority = prompt_priority("Priority (HIGH/MID/LOW): ")
    item = todo_manager.add_item(
        owner=username,
        title=title,
        details=details,
        priority=priority,
    )
    print(f"Created to-do item {item.id}.")


def handle_edit(todo_manager: TodoManager, username: str) -> None:
    print("\n=== Edit To-Do ===")
    item_id = prompt_non_empty("Enter item ID: ")
    item = todo_manager.get_item(item_id, username)
    if item is None:
        print("To-do item not found.")
        return

    title = prompt_optional(f"Title [{item.title}]: ")
    details = prompt_optional(f"Details [{item.details}]: ")
    priority = prompt_priority(
        f"Priority ({item.priority.value}) [HIGH/MID/LOW]: ", allow_blank=True
    )
    status = prompt_status(
        f"Status ({item.status.value}) [PENDING/COMPLETED]: ", allow_blank=True
    )

    updates = {}
    if title:
        updates["title"] = title
    if details:
        updates["details"] = details
    if priority is not None:
        updates["priority"] = priority
    if status is not None:
        updates["status"] = status

    if not updates:
        print("No changes provided.")
        return

    updated_item = todo_manager.update_item(item_id, username, updates)
    if updated_item is None:
        print("Unable to update to-do item.")
        return
    print("To-do item updated.")


def handle_list(todo_manager: TodoManager, username: str) -> None:
    print("\n=== Your To-Do Items ===")
    items = todo_manager.list_items(username)
    if not items:
        print("No to-do items found.")
        return
    for item in items:
        show_item_summary(item)


def handle_details(todo_manager: TodoManager, username: str) -> None:
    print("\n=== View To-Do Details ===")
    item_id = prompt_non_empty("Enter item ID: ")
    item = todo_manager.get_item(item_id, username)
    if item is None:
        print("To-do item not found.")
        return
    show_item_details(item)


def handle_mark_completed(todo_manager: TodoManager, username: str) -> None:
    print("\n=== Mark To-Do Completed ===")
    item_id = prompt_non_empty("Enter item ID: ")
    item = todo_manager.mark_completed(item_id, username)
    if item is None:
        print("To-do item not found.")
        return
    print("To-do item marked as completed.")


def handle_logged_in_loop(
    todo_manager: TodoManager, username: str
) -> Callable[[], bool]:
    def loop() -> bool:
        choice = prompt_logged_in_choice(username)
        if choice == "1":
            handle_create(todo_manager, username)
            return True
        if choice == "2":
            handle_edit(todo_manager, username)
            return True
        if choice == "3":
            handle_list(todo_manager, username)
            return True
        if choice == "4":
            handle_details(todo_manager, username)
            return True
        if choice == "5":
            handle_mark_completed(todo_manager, username)
            return True
        if choice == "6":
            print("Logged out.")
            return False
        if choice == "7":
            print("Goodbye.")
            raise SystemExit(0)

        print("Invalid option. Please try again.")
        return True

    return loop


def main() -> None:
    data_dir = Path(__file__).resolve().parent.parent
    auth_manager = AuthManager(data_dir / "users.json")
    todo_manager = TodoManager(data_dir / "todos.json")

    while True:
        choice = prompt_prelogin_choice()
        if choice == "1":
            username = handle_login(auth_manager)
            if username is None:
                continue
            logged_in_loop = handle_logged_in_loop(todo_manager, username)
            while logged_in_loop():
                pass
            continue
        if choice == "2":
            handle_signup(auth_manager)
            continue
        if choice == "3":
            print("Goodbye.")
            break

        print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
