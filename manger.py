import json
from intern import Intern
from utils import Status, DATA_FILE
from typing import Dict, List


def load_interns() -> Dict[str, Intern]:
    try:
        with open(DATA_FILE, "r") as file:
            raw = json.load(file)
        return {k: Intern.from_dict(v) for k, v in raw.items()}
    except FileNotFoundError:
        return {}


def save_interns(interns: Dict[str, Intern]):
    with open(DATA_FILE, "w") as file:
        json.dump({k: v.to_dict() for k, v in interns.items()}, file, indent=4)


def generate_intern_id(interns: Dict[str, Intern]) -> str:
    return f"INT{len(interns) + 1:03d}"

def add_intern(interns: Dict[str, Intern]):
    name = input("Name: ")
    role = input("Role: ")

    try:
        daily_hours = int(input("Expected daily hours: "))
        daily_tasks = int(input("Expected daily tasks: "))
    except ValueError:
        print("Invalid numeric input.")
        return

    intern_id = generate_intern_id(interns)
    interns[intern_id] = Intern(
        intern_id, name, role, daily_hours, daily_tasks
    )
    save_interns(interns)
    print(f"Intern added with ID {intern_id}")


def add_daily_activity(interns: Dict[str, Intern]):
    intern_id = input("Enter Intern ID: ")

    intern = interns.get(intern_id)
    if not intern:
        print("Intern not found.")
        return

    if intern.status != Status.ACTIVE:
        print("Activity allowed only for ACTIVE interns.")
        return

    try:
        hours = int(input("Hours worked: "))
        if hours < 0:
            raise ValueError
        task = input("Task description: ").strip()
        if not task:
            raise ValueError
    except ValueError:
        print("Invalid input. Entry skipped.")
        return

    intern.hours.append(hours)
    intern.tasks.append(task)
    save_interns(interns)
    print("Activity recorded.")


def update_intern_status(interns: Dict[str, Intern]):
    intern_id = input("Enter Intern ID: ")
    intern = interns.get(intern_id)

    if not intern:
        print("Intern not found.")
        return

    print("1. Active")
    print("2. Inactive")
    print("3. Completed")

    choice = input("Select new status: ")

    if choice == "1":
        intern.status = Status.ACTIVE
    elif choice == "2":
        intern.status = Status.INACTIVE
    elif choice == "3":
        intern.status = Status.COMPLETED
    else:
        print("Invalid choice.")
        return

    save_interns(interns)
    print("Status updated.")


def view_intern_summary(interns: Dict[str, Intern]):
    intern_id = input("Enter Intern ID: ")
    intern = interns.get(intern_id)

    if not intern:
        print("Intern not found.")
        return

    intern.summary()


def overall_statistics(interns: Dict[str, Intern]):
    if not interns:
        print("No interns available.")
        return

    total_interns = len(interns)
    active_interns = sum(1 for i in interns.values() if i.status == Status.ACTIVE)

    total_hours = sum(i.total_hours() for i in interns.values())
    total_days = sum(len(i.hours) for i in interns.values())
    avg_hours = total_hours / total_days if total_days else 0

    top = max(interns.values(), key=lambda i: i.total_hours(), default=None)

    print("\n====== OVERALL STATISTICS ======")
    print(f"Total Interns     : {total_interns}")
    print(f"Active Interns    : {active_interns}")
    print(f"Average Hours     : {avg_hours:.2f}")
    if top:
        print(f"Top Performer     : {top.name} ({top.total_hours()} hrs)")
    print("===============================\n")


