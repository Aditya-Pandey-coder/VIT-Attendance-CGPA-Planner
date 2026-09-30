# VIT Attendance & CGPA Planner

A small command-line app I built to stop doing attendance and CGPA math on my phone calculator every other week.

At VIT you need 75% attendance in every course to be eligible for the exam, and your CGPA depends on credits and grades across semesters. Most of us track this in our heads, in a notes app, or in some half-broken spreadsheet. None of those actually tell you the two things you really want to know: *how many more classes can I bunk?* and *what do I need to score next sem to hit my target CGPA?*

This app answers both. Everything runs in the terminal and your data sits in a plain JSON file, so there's no setup, no database and no internet needed.

## What it does

The program is split into four parts, all reachable from one menu.

**Course manager.** Add, view, edit and delete courses. Each course has a code, a name and its credits. Input is checked as you type, so you can't enter negative credits or leave the name blank, and you can't add the same course code twice.

**Attendance tracker.** Log a class as attended or missed, and it recalculates your percentage right away. If you drop below 75% it warns you. It also tells you one of two things: how many classes you can still skip and stay eligible, or how many you now have to attend in a row to get back to 75%.

**GPA / CGPA calculator.** Enter grades and it works out your semester GPA and overall CGPA using the VIT scale (S=10, A=9, B=8, C=7, D=6, E=5, F=0). There's also a target predictor: give it the CGPA you want and it tells you what GPA you need next semester. If the answer is above 10, it says the target isn't reachable instead of giving you a nonsense number.

**Reports.** A summary table of all your courses in the terminal, and an option to export the same thing to a text file.

## Project layout

```
attendance-cgpa-planner/
├── main.py              # menu loop only, no logic in here
├── models.py            # Course class
├── storage.py           # load/save JSON
├── validators.py        # input helpers
├── course_manager.py    # module 1
├── attendance.py        # module 2
├── gpa_calculator.py    # module 3
├── reports.py           # module 4
├── logger.py            # logging setup
├── data/courses.json    # your saved data
├── tests/
│   ├── test_attendance.py
│   └── test_gpa.py
├── README.md
└── statement.md         # problem statement
```

I tried to keep `main.py` as dumb as possible. It only shows the menu and calls into the other files. All the actual rules live in the module files, which made testing a lot easier.

## Running it

You need Python 3.8 or newer. There are no external packages for the app itself.

```bash
git clone https://github.com/<your-username>/attendance-cgpa-planner.git
cd attendance-cgpa-planner
python main.py
```

Then pick an option from the menu. On the first run the `data/courses.json` file is created for you if it isn't there.

## How the numbers are worked out

I wanted these to be correct, so here's the math I used.

- **Attendance %** = attended / held × 100. If no classes have been held yet it returns 0 instead of crashing on a divide by zero.
- **Classes you can skip** = `max(0, (4 * attended - 3 * held) // 3)`. This comes from solving attended / (held + x) ≥ 0.75 for x.
- **Classes you must attend** = `max(0, 3 * held - 4 * attended)`. This comes from (attended + y) / (held + y) ≥ 0.75.
- **GPA** = Σ(credits × grade point) / Σ(credits). CGPA uses the same formula, just across every semester.
- **Required GPA for a target** = (target × (C_done + C_new) − CGPA × C_done) / C_new, where C_done is credits finished and C_new is credits next semester.

The skip and attend formulas use integer math on purpose. With floats you can end up at 74.99999 when you're really at exactly 75, and that would give the wrong answer at the boundary.

The 75% threshold and the grade table are both defined once as constants, so if VIT changes the rules you only edit one spot.

## Data and reliability

Courses are saved to `data/courses.json`. When saving, the app writes to a temp file first and then swaps it in with `os.replace`, so if it crashes halfway through a write your old data is still there. If the JSON file is missing or corrupted, the app starts with an empty list and logs a warning instead of blowing up.

Errors and important actions go to a log file, which helps when something odd happens and you want to see what led to it.

## Tests

There are around a dozen tests covering the edge cases I was most worried about:

- zero classes held
- exactly 75% and just below it (74.9%)
- skip and must-attend boundaries
- all S grades giving a GPA of 10.0
- courses with mixed credits
- a target CGPA that can't be reached
- a corrupt JSON file
- duplicate course codes

Run them from the project folder:

```bash
python -m pytest tests/
```

If you don't have pytest, `pip install pytest` will sort it out.

## Limitations

- It's a terminal app, so no GUI. That was a choice, not an accident.
- Attendance is tracked as totals per course, not per date, so you can't see which specific days you missed.
- It assumes the VIT grading scale and 75% rule. Other colleges would need to change the constants.

## Ideas for later

- Track attendance by date
- Import a timetable
- Support more than one student profile

## Author

Made by [Your Name], [Your Reg. No.], for my Python course project at VIT.
