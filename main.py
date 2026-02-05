from intern import Intern

def main():
    print("Enter Intern Details")
    name = input("Name: ")
    role = input("Role: ")

    try:
        daily_hours = int(input("Expected daily hours: "))
        daily_tasks = int(input("Expected daily tasks: "))
    except ValueError:
        print("Invalid numeric input.")
        return

    intern = Intern(name, role, daily_hours, daily_tasks)

    intern.log_activity()
    intern.calculate_stat()
    intern.store_stat()
    intern.summary()

main()
