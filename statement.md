# Problem Statement

Students at VIT have to track attendance per course against the 75% eligibility rule,
and calculate GPA and CGPA from credits and grades. They usually do this by hand or
with scattered calculators. Nothing shows them how many classes they can still miss,
or what grade they need to reach a target CGPA.

# Solution

VIT Attendance & CGPA Planner - a menu-driven CLI app (Python) that stores everything
in a JSON file.

## Modules
1. **Course manager** - add, view, edit, delete courses (name, code, credits, semester) with input validation.
2. **Attendance tracker** - log classes attended/held, compute percentage, warn below 75%, and report how many classes can be skipped or must be attended to stay eligible.
3. **GPA/CGPA calculator** - grade scale S=10, A=9, B=8, C=7, D=6, E=5, F=0; semester GPA, CGPA, and a target-CGPA predictor.
4. **Reports** - summary table of all courses and a text report exported to a file.

## Non-functional requirements
- Input validation and error handling on every prompt
- Reliable JSON persistence (atomic writes, corrupt-file recovery)
- Logging to a file
- Modular, maintainable structure with configurable rules in one place
- Fast response and low memory use (pure standard library, no external dependencies)
- Unit tests covering edge cases
