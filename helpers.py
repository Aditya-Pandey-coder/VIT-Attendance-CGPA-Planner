# Input functions. Each one keeps asking until the user types a valid value.
from config import GRADES


def get_text(prompt):
    while True:
        text = input(prompt).strip()
        if text != "":
            return text
        print("  Input cannot be empty.")


def get_int(prompt, low=None, high=None):
    while True:
        try:
            num = int(input(prompt).strip())
        except ValueError:
            print("  Please enter a whole number.")
            continue
        if low is not None and num < low:
            print("  Value must be at least", low)
        elif high is not None and num > high:
            print("  Value must be at most", high)
        else:
            return num


def get_float(prompt, low=None, high=None):
    while True:
        try:
            num = float(input(prompt).strip())
        except ValueError:
            print("  Please enter a number.")
            continue
        if low is not None and num < low:
            print("  Value must be at least", low)
        elif high is not None and num > high:
            print("  Value must be at most", high)
        else:
            return num


def get_grade(prompt):
    while True:
        grade = input(prompt).strip().upper()
        if grade in GRADES:
            return grade
        print("  Grade must be one of:", ", ".join(GRADES))


def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please answer y or n.")
