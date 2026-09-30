# Module 1: add, view, edit and delete courses.
import helpers
import storage
from logger import log
from models import make_course


def find_course(courses, code):
    code = str(code).strip().upper()
    for c in courses:
        if c["code"] == code:
            return c
    return None


def add_course(courses, course):
    if find_course(courses, course["code"]) is not None:
        raise ValueError("Course " + course["code"] + " already exists.")
    courses.append(course)
    log.info("Added course %s", course["code"])


def delete_course(courses, code):
    c = find_course(courses, code)
    if c is None:
        return False
    courses.remove(c)
    log.info("Deleted course %s", c["code"])
    return True


def edit_course(courses, code, name=None, credits=None, semester=None):
    c = find_course(courses, code)
    if c is None:
        raise KeyError("Course " + str(code) + " not found.")
    # build the new version first so a bad value can't half-change the course
    new = make_course(c["code"],
                      c["name"] if name is None else name,
                      c["credits"] if credits is None else credits,
                      c["semester"] if semester is None else semester,
                      c["held"], c["attended"], c["grade"])
    c.update(new)
    log.info("Edited course %s", c["code"])


def show_courses(courses):
    if len(courses) == 0:
        print("  No courses added yet.")
        return
    print("  %-10s%-32s%7s%5s" % ("Code", "Name", "Credits", "Sem"))
    print("  " + "-" * 54)
    for c in sorted(courses, key=lambda x: (x["semester"], x["code"])):
        print("  %-10s%-32s%7d%5d" % (c["code"], c["name"][:30], c["credits"], c["semester"]))


def pick_course(courses):
    """Ask for a course code. Returns the course, or None if the user cancels."""
    if len(courses) == 0:
        print("  No courses added yet.")
        return None
    while True:
        code = input("  Course code (blank to cancel): ").strip()
        if code == "":
            return None
        c = find_course(courses, code)
        if c is not None:
            return c
        print("  Course not found.")


def add_menu(courses):
    code = helpers.get_text("  Course code: ")
    if find_course(courses, code):
        print("  That course already exists.")
        return
    name = helpers.get_text("  Course name: ")
    credits = helpers.get_int("  Credits (0-30): ", 0, 30)
    semester = helpers.get_int("  Semester (1-20): ", 1, 20)
    add_course(courses, make_course(code, name, credits, semester))
    storage.save_courses(courses)
    print("  Course added.")


def edit_menu(courses):
    c = pick_course(courses)
    if c is None:
        return
    print("  Press Enter to keep the current value.")
    name = input("  Name [%s]: " % c["name"]).strip() or None
    credits = input("  Credits [%d]: " % c["credits"]).strip()
    semester = input("  Semester [%d]: " % c["semester"]).strip()
    try:
        credits = int(credits) if credits else None
        semester = int(semester) if semester else None
        edit_course(courses, c["code"], name, credits, semester)
    except ValueError as err:
        print("  Edit rejected:", err)
        return
    storage.save_courses(courses)
    print("  Course updated.")


def delete_menu(courses):
    c = pick_course(courses)
    if c is None:
        return
    if helpers.ask_yes_no("  Delete %s - %s? (y/n): " % (c["code"], c["name"])):
        delete_course(courses, c["code"])
        storage.save_courses(courses)
        print("  Course deleted.")


def run_menu(courses):
    while True:
        print("\n--- Course Manager ---")
        print("1. Add course")
        print("2. View courses")
        print("3. Edit course")
        print("4. Delete course")
        print("0. Back")
        choice = helpers.get_int("Choice: ", 0, 4)
        if choice == 0:
            return
        elif choice == 1:
            add_menu(courses)
        elif choice == 2:
            show_courses(courses)
        elif choice == 3:
            edit_menu(courses)
        else:
            delete_menu(courses)
