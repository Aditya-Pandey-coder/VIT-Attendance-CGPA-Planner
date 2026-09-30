# VIT Attendance & CGPA Planner

A menu-driven Python program that tracks attendance against the 75% rule,
calculates GPA / CGPA, and works out the GPA needed to reach a target CGPA.
Courses are saved in `data/courses.json`. Only the Python standard library is
used (Python 3.8+), so nothing needs to be installed.

## Run
    python main.py

## Test
    python -m unittest discover -s tests -v

## Features
- **Course manager** - add, view, edit, delete courses (code, name, credits, semester). Duplicate codes are rejected.
- **Attendance tracker** - log a class or set the totals. Shows the percentage, warns below 75%, and says how many classes you can skip or must attend.
- **GPA / CGPA** - assign grades (S=10, A=9, B=8, C=7, D=6, E=5, F=0), see semester GPA and CGPA, and use the target CGPA predictor.
- **Reports** - summary table on screen and a text report saved to `report.txt`.

## Formulas
- Attendance % = attended / held x 100
- Can skip = (100a - T*h) // T (never below 0)
- Must attend = ceil((T*h - 100a) / (100 - T)) (T is the threshold, 75)
- GPA = sum(credits x grade points) / sum(credits), courses with no grade are ignored
- Required GPA = (target x (done + new) - CGPA x done) / new. If this is above 10 the target cannot be reached.

## Files
    main.py        main menu
    config.py      threshold, grade table, file paths
    models.py      make_course() - builds and checks a course dictionary
    helpers.py     input functions that repeat until the value is valid
    storage.py     save / load JSON (safe write, corrupt file recovery)
    courses.py     course manager
    attendance.py  attendance tracker
    gpa.py         GPA / CGPA calculator
    reports.py     reports
    logger.py      logging to logs/app.log
    tests/         unit tests

## Safety
- Saving writes a temp file first and then replaces the real file, so a crash cannot wipe the data.
- A corrupt data file is renamed to `courses.json.corrupt` and the program starts fresh.
- Bad records inside the file are skipped and written to the log.
