# A course is stored as a plain dictionary. make_course checks the values.
from config import GRADES


def make_course(code, name, credits, semester=1, held=0, attended=0, grade=None):
    code = str(code).strip().upper()
    name = str(name).strip()
    if grade is not None:
        grade = str(grade).strip().upper()
        if grade == "":
            grade = None

    if code == "":
        raise ValueError("Course code cannot be empty.")
    if name == "":
        raise ValueError("Course name cannot be empty.")
    if grade is not None and grade not in GRADES:
        raise ValueError("Invalid grade: " + grade)
    if credits < 0 or credits > 30:
        raise ValueError("Credits must be between 0 and 30.")
    if semester < 1:
        raise ValueError("Semester must be 1 or more.")
    if held < 0 or attended < 0:
        raise ValueError("Attendance cannot be negative.")
    if attended > held:
        raise ValueError("Attended cannot be more than held.")

    return {"code": code, "name": name, "credits": credits, "semester": semester,
            "held": held, "attended": attended, "grade": grade}
