# Module 2: attendance percentage, classes to skip / attend, logging classes.
# Whole-number maths is used so there are no float rounding problems.
import helpers
import storage
from config import THRESHOLD
from courses import pick_course
from logger import log


def percentage(course):
    if course["held"] == 0:
        return 0.0
    return course["attended"] * 100 / course["held"]


def is_eligible(course):
    # attended / held >= THRESHOLD / 100
    return 100 * course["attended"] >= THRESHOLD * course["held"]


def can_skip(course):
    # attended / (held + x) >= THRESHOLD / 100  =>  x <= (100a - T*h) / T
    x = (100 * course["attended"] - THRESHOLD * course["held"]) // THRESHOLD
    return max(0, x)


def must_attend(course):
    # (attended + y) / (held + y) >= THRESHOLD / 100  =>  y >= (T*h - 100a) / (100 - T)
    need = THRESHOLD * course["held"] - 100 * course["attended"]
    if need <= 0:
        return 0
    gap = 100 - THRESHOLD
    return (need + gap - 1) // gap  # round up


def log_class(course, present):
    course["held"] += 1
    if present:
        course["attended"] += 1
    log.info("Logged class for %s (present=%s)", course["code"], present)


def status(course):
    if course["held"] == 0:
        return course["code"] + ": no classes logged yet"
    text = "%s: %.1f%% (%d/%d)" % (course["code"], percentage(course),
                                   course["attended"], course["held"])
    if is_eligible(course):
        return text + " - OK, you can skip %d more class(es)" % can_skip(course)
    return text + " - WARNING: below %d%%, attend the next %d class(es)" % (
        THRESHOLD, must_attend(course))


def log_menu(courses):
    c = pick_course(courses)
    if c is None:
        return
    present = helpers.ask_yes_no("  Were you present? (y/n): ")
    log_class(c, present)
    storage.save_courses(courses)
    print("  " + status(c))


def set_menu(courses):
    c = pick_course(courses)
    if c is None:
        return
    held = helpers.get_int("  Total classes held: ", 0)
    attended = helpers.get_int("  Classes attended: ", 0, held)
    c["held"] = held
    c["attended"] = attended
    log.info("Set attendance for %s to %d/%d", c["code"], attended, held)
    storage.save_courses(courses)
    print("  " + status(c))


def show_all(courses):
    if len(courses) == 0:
        print("  No courses added yet.")
    for c in courses:
        print("  " + status(c))


def run_menu(courses):
    while True:
        print("\n--- Attendance Tracker ---")
        print("1. Log a class")
        print("2. Set totals (held / attended)")
        print("3. Show status of all courses")
        print("0. Back")
        choice = helpers.get_int("Choice: ", 0, 3)
        if choice == 0:
            return
        elif choice == 1:
            log_menu(courses)
        elif choice == 2:
            set_menu(courses)
        else:
            show_all(courses)
