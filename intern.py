import json
from typing import Dict, List
from utils import Status

class Intern:
    def __init__(self, intern_id: str, name: str, role: str,
                 daily_hours: int, daily_tasks: int):
        self.intern_id = intern_id
        self.name = name.strip().title()
        self.role = role.strip().title()
        self.daily_hours = daily_hours
        self.daily_tasks = daily_tasks
        self.status = Status.ACTIVE
        self.hours: List[int] = []
        self.tasks: List[str] = []

    def total_hours(self) -> int:
        return sum(self.hours)

    def average_hours(self) -> float:
        return self.total_hours() / len(self.hours) if self.hours else 0

    def to_dict(self) -> dict:
        return {
            "intern_id": self.intern_id,
            "name": self.name,
            "role": self.role,
            "daily_hours": self.daily_hours,
            "daily_tasks": self.daily_tasks,
            "status": self.status.value,
            "daily_work": [
                {"hours": h, "task": t}
                for h, t in zip(self.hours, self.tasks)
            ]
        }

    @staticmethod
    def from_dict(data: dict):
        intern = Intern(
            data["intern_id"],
            data["name"],
            data["role"],
            data["daily_hours"],
            data["daily_tasks"]
        )
        intern.status = Status(data["status"])
        for entry in data["daily_work"]:
            intern.hours.append(entry["hours"])
            intern.tasks.append(entry["task"])
        return intern

    def summary(self):
        print("\n====== INTERN SUMMARY ======")
        print(f"ID             : {self.intern_id}")
        print(f"Name           : {self.name}")
        print(f"Role           : {self.role}")
        print(f"Status         : {self.status.value}")
        print(f"Days Worked    : {len(self.hours)}")
        print(f"Total Hours    : {self.total_hours()}")
        print(f"Average Hours  : {self.average_hours():.2f}")
        if self.tasks:
            print(f"Last Task      : {self.tasks[-1]}")
        print("============================")






