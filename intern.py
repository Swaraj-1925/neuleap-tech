import json

class Intern:
    name: str
    role: str
    daily_hours: int
    daily_tasks: int

    def __init__(self, name: str, role: str, daily_hours: int, daily_tasks: int):
        self.name = name.strip().capitalize()
        self.role = role.strip().capitalize()
        self.daily_hours = daily_hours
        self.daily_tasks = daily_tasks

        self.hours = []
        self.tasks = []
        self.total_hours = 0
        self.avg_hours = 0

    def log_activity(self):
        try:
            days_worked = int(input("Enter number of days to record: "))
            if days_worked <= 0:
                raise ValueError
        except ValueError:
            print("Invalid number of days.")
            return

        for day in range(1, days_worked + 1):
            try:
                hours = int(input(f"Hours worked on day {day}: "))
                if hours < 0:
                    raise ValueError("Hours must be non-negative")

                task = input(f"Task done on day {day}: ").strip()
                if not task:
                    raise ValueError("Task description cannot be empty")

                self.hours.append(hours)
                self.tasks.append(task)

            except ValueError as e:
                print("Skipping entry:", e)

    def calculate_stat(self):
        self.total_hours = sum(self.hours)
        self.avg_hours = self.total_hours / len(self.hours) if self.hours else 0

    def store_stat(self):
        data = {
            "name": self.name,
            "role": self.role,
            "daily_work": [
                {"hours_worked": h, "task": t}
                for h, t in zip(self.hours, self.tasks)
            ]
        }

        with open(f"{self.name}.json", "w") as file:
            json.dump(data, file, indent=4)

        print(f"Data saved to {self.name}.json")

    def load_stat(self, path: str):
        with open(path, "r") as file:
            data = json.load(file)

        self.name = data["name"]
        self.role = data["role"]
        self.hours.clear()
        self.tasks.clear()

        for entry in data["daily_work"]:
            self.hours.append(entry["hours_worked"])
            self.tasks.append(entry["task"])

    def summary(self):
        print("\n====== INTERN SUMMARY ======")
        print(f"Name           : {self.name}")
        print(f"Role           : {self.role}")
        print(f"Days Worked    : {len(self.hours)}")
        print(f"Total Hours    : {self.total_hours}")
        print(f"Average Hours  : {self.avg_hours:.2f}")
        print("============================\n")























