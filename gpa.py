# Module 3: GPA, CGPA and the target CGPA predictor.
import helpers
import storage
from config import GRADES, MAX_GPA
from courses import pick_course


def graded_credits(courses):
    total = 0
    for c in courses:
        if c["grade"] is not None:
            total += c["credits"]
    return total


def gpa(courses):
    """Credit-weighted average of grade points. Courses without a grade are ignored."""
    credits = graded_credits(courses)
    if credits == 0:
        return 0.0
    points = 0
    for c in courses:
        if c["grade"] is not None:
            points += c["credits"] * GRADES[c["grade"]]
    return points / credits


def cgpa(courses):
    # same formula as GPA, just over the courses of every semester
    return gpa(courses)


def by_semester(courses):
    groups = {}
    for c in courses:
        groups.setdefault(c["semester"], []).append(c)
    return groups


def required_gpa(target, current_cgpa, credits_done, credits_new):
    if credits_new <= 0:
        raise ValueError("Next semester credits must be positive.")
    total = target * (credits_done + credits_new)
    return (total - current_cgpa * credits_done) / credits_new


def is_reachable(required):
    return required <= MAX_GPA


def minimum_grade(required):
    """Lowest grade that gives at least `required` points, or None if impossible."""
    if not is_reachable(required):
        return None
    best = None
    for grade, points in GRADES.items():
        if points >= required and (best is None or points < GRADES[best]):
            best = grade
    return best


def assign_grade(courses):
    c = pick_course(courses)
    if c is None:
        return
    c["grade"] = helpers.get_grade("  Grade for %s (%s): " % (c["code"], "/".join(GRADES)))
    storage.save_courses(courses)
    print("  %s graded %s." % (c["code"], c["grade"]))


def show_gpa(courses):
    if len(courses) == 0:
        print("  No courses added yet.")
        return
    groups = by_semester(courses)
    for sem in sorted(groups):
        if graded_credits(groups[sem]) > 0:
            print("  Semester %d GPA: %.2f" % (sem, gpa(groups[sem])))
        else:
            print("  Semester %d: no graded courses" % sem)
    print("  CGPA: %.2f (%d graded credits)" % (cgpa(courses), graded_credits(courses)))


def predict(courses):
    done = graded_credits(courses)
    if done == 0:
        print("  Grade some courses first so a current CGPA exists.")
        return
    current = cgpa(courses)
    print("  Current CGPA: %.2f over %d credits" % (current, done))
    target = helpers.get_float("  Target CGPA (0-10): ", 0, 10)
    new_credits = helpers.get_int("  Credits you will take next semester: ", 1, 60)

    need = required_gpa(target, current, done, new_credits)
    if not is_reachable(need):
        print("  Target unreachable: you would need a GPA of %.2f (max is %d)." % (need, MAX_GPA))
    elif need <= 0:
        print("  Target already secured - any results keep you at or above it.")
    else:
        print("  You need a GPA of %.2f next semester (roughly all '%s' grades or better)."
              % (need, minimum_grade(need)))


def run_menu(courses):
    while True:
        print("\n--- GPA / CGPA Calculator ---")
        print("1. Assign / change a grade")
        print("2. Show GPA and CGPA")
        print("3. Target CGPA predictor")
        print("0. Back")
        choice = helpers.get_int("Choice: ", 0, 3)
        if choice == 0:
            return
        elif choice == 1:
            assign_grade(courses)
        elif choice == 2:
            show_gpa(courses)
        else:
            predict(courses)
