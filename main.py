# VIT Attendance & CGPA Planner - starts the program and shows the main menu.
import attendance
import courses
import gpa
import helpers
import reports
import storage
from logger import log


def main():
    all_courses = storage.load_courses()
    log.info("Application started")
    try:
        while True:
            print("\n==== VIT Attendance & CGPA Planner ====")
            print("1. Course manager")
            print("2. Attendance tracker")
            print("3. GPA / CGPA calculator")
            print("4. Reports")
            print("0. Exit")
            choice = helpers.get_int("Choice: ", 0, 4)
            if choice == 0:
                break
            elif choice == 1:
                courses.run_menu(all_courses)
            elif choice == 2:
                attendance.run_menu(all_courses)
            elif choice == 3:
                gpa.run_menu(all_courses)
            else:
                reports.run_menu(all_courses)
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        storage.save_courses(all_courses)
        log.info("Application exited")
    print("Goodbye!")


if __name__ == "__main__":
    main()
