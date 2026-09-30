# Settings that may change later are kept here.
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "courses.json")
LOG_FILE = os.path.join(BASE_DIR, "logs", "app.log")
REPORT_FILE = os.path.join(BASE_DIR, "report.txt")

# minimum attendance % needed to write the exam
THRESHOLD = 75

# VIT grade scale
GRADES = {"S": 10, "A": 9, "B": 8, "C": 7, "D": 6, "E": 5, "F": 0}
MAX_GPA = 10
