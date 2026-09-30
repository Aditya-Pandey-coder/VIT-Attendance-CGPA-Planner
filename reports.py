# Module 4: summary table and text report.
from datetime import datetime

import config
import helpers
from attendance import is_eligible, percentage
from gpa import by_semester, cgpa, gpa, graded_credits
from logger import log

HEADERS = ["Code", "Name", "Sem", "Cr", "Held", "Att", "Att %", "Grade", "Status"]


def make_row(c):
    if c["held"] == 0:
        status = "-"
    elif is_eligible(c):
        status = "OK"
    else:
        status = "LOW"
    return [c["code"], c["name"][:24], str(c["semester"]), str(c["credits"]),
            str(c["held"]), str(c["attended"]), "%.1f" % percentage(c),
            c["grade"] or "-", status]


def summary_table(courses):
    if len(courses) == 0:
        return "No courses added yet."
    rows = [HEADERS]
    for c in sorted(courses, key=lambda x: (x["semester"], x["code"])):
        rows.append(make_row(c))

    # each column is as wide as its longest cell
    widths = []
    for i in range(len(HEADERS)):
        widths.append(max(len(r[i]) for r in rows))

    lines = []
    for n, r in enumerate(rows):
        cells = [r[i].ljust(widths[i]) for i in range(len(r))]
        lines.append(" | ".join(cells))
        if n == 0:
            lines.append("-+-".join("-" * w for w in widths))
    return "\n".join(lines)


def build_report(courses):
    lines = ["VIT ATTENDANCE & CGPA PLANNER - REPORT",
             "Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M"),
             "",
             summary_table(courses),
             ""]
    groups = by_semester(courses)
    for sem in sorted(groups):
        if graded_credits(groups[sem]) > 0:
            lines.append("Semester %d GPA: %.2f" % (sem, gpa(groups[sem])))
        else:
            lines.append("Semester %d GPA: n/a" % sem)
    lines.append("CGPA: %.2f (%d graded credits)" % (cgpa(courses), graded_credits(courses)))

    low = [c["code"] for c in courses if c["held"] > 0 and not is_eligible(c)]
    lines.append("")
    lines.append("Courses below %d%% attendance: %s" % (
        config.THRESHOLD, ", ".join(low) if low else "none"))
    return "\n".join(lines) + "\n"


def export_report(courses, path=None):
    path = path or config.REPORT_FILE
    with open(path, "w", encoding="utf-8") as f:
        f.write(build_report(courses))
    log.info("Report exported to %s", path)
    return path


def run_menu(courses):
    while True:
        print("\n--- Reports ---")
        print("1. Print summary table")
        print("2. Export text report")
        print("0. Back")
        choice = helpers.get_int("Choice: ", 0, 2)
        if choice == 0:
            return
        elif choice == 1:
            print(summary_table(courses))
        else:
            path = input("  File path [report.txt]: ").strip()
            try:
                print("  Report saved to", export_report(courses, path or None))
            except OSError as err:
                print("  Could not write report:", err)
