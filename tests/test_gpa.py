import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gpa as g
import reports
from models import make_course


def c(code, credits, grade, sem=1):
    return make_course(code, code, credits, semester=sem, grade=grade)


class TestGPA(unittest.TestCase):
    def test_all_s_grades_gives_10(self):
        self.assertEqual(g.gpa([c("A", 4, "S"), c("B", 3, "S")]), 10.0)

    def test_mixed_credits(self):
        lst = [c("A", 4, "S"), c("B", 3, "B"), c("C", 2, "D")]
        self.assertAlmostEqual(g.gpa(lst), 76 / 9)  # (40+24+12)/9

    def test_f_counts_credits_as_zero_points(self):
        self.assertAlmostEqual(g.gpa([c("A", 4, "S"), c("B", 4, "F")]), 5.0)

    def test_ungraded_courses_ignored(self):
        self.assertEqual(g.gpa([c("A", 4, "A"), c("B", 4, None)]), 9.0)
        self.assertEqual(g.gpa([c("B", 4, None)]), 0.0)

    def test_cgpa_across_semesters(self):
        lst = [c("A", 4, "S", 1), c("B", 2, "E", 2)]
        self.assertAlmostEqual(g.cgpa(lst), 50 / 6)

    def test_required_gpa_reachable(self):
        need = g.required_gpa(8.5, 8.0, 20, 20)
        self.assertAlmostEqual(need, 9.0)
        self.assertTrue(g.is_reachable(need))
        self.assertEqual(g.minimum_grade(need), "A")

    def test_unreachable_target(self):
        need = g.required_gpa(9.9, 7.0, 40, 10)
        self.assertGreater(need, 10)
        self.assertFalse(g.is_reachable(need))
        self.assertIsNone(g.minimum_grade(need))

    def test_required_gpa_needs_positive_credits(self):
        with self.assertRaises(ValueError):
            g.required_gpa(8, 8, 20, 0)


class TestReports(unittest.TestCase):
    def test_empty_report(self):
        self.assertEqual(reports.summary_table([]), "No courses added yet.")
        self.assertIn("CGPA: 0.00", reports.build_report([]))

    def test_report_lists_low_attendance(self):
        lst = [make_course("CS1", "Intro", 4, held=10, attended=5, grade="A")]
        text = reports.build_report(lst)
        self.assertIn("LOW", text)
        self.assertIn("below 75% attendance: CS1", text)


if __name__ == "__main__":
    unittest.main()
