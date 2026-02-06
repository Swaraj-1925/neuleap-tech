from manger import load_interns, add_intern, add_daily_activity, update_intern_status, view_intern_summary, overall_statistics

def main():
    interns = load_interns()

    while True:
        print("\n--- Intern Management System ---")
        print("1. Add Intern")
        print("2. Add Daily Activity")
        print("3. Update Intern Status")
        print("4. View Intern Summary")
        print("5. Overall Statistics")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_intern(interns)
        elif choice == "2":
            add_daily_activity(interns)
        elif choice == "3":
            update_intern_status(interns)
        elif choice == "4":
            view_intern_summary(interns)
        elif choice == "5":
            overall_statistics(interns)
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice.")

main()
