import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import attendance as att
import courses as cm
import storage
from models import make_course


def mk(held, attended, code="CS101"):
    return make_course(code, "Test", 3, held=held, attended=attended)


class TestAttendance(unittest.TestCase):
    def test_zero_classes_held(self):
        c = mk(0, 0)
        self.assertEqual(att.percentage(c), 0.0)
        self.assertTrue(att.is_eligible(c))
        self.assertEqual(att.must_attend(c), 0)

    def test_exactly_75_percent(self):
        c = mk(4, 3)
        self.assertAlmostEqual(att.percentage(c), 75.0)
        self.assertTrue(att.is_eligible(c))
        self.assertEqual(att.can_skip(c), 0)
        self.assertEqual(att.must_attend(c), 0)

    def test_74_9_percent(self):
        c = mk(1000, 749)
        self.assertFalse(att.is_eligible(c))
        self.assertEqual(att.must_attend(c), 4)  # 753/1004 = 75%

    def test_can_skip(self):
        c = mk(10, 10)
        self.assertEqual(att.can_skip(c), 3)  # 10/13 ok, 10/14 not
        c["held"] += 3
        self.assertTrue(att.is_eligible(c))
        c["held"] += 1
        self.assertFalse(att.is_eligible(c))

    def test_must_attend(self):
        c = mk(10, 5)
        y = att.must_attend(c)
        self.assertEqual(y, 10)
        self.assertGreaterEqual(100 * (5 + y), 75 * (10 + y))
        self.assertLess(100 * (5 + y - 1), 75 * (10 + y - 1))
        self.assertEqual(att.can_skip(c), 0)

    def test_log_class(self):
        c = mk(0, 0)
        att.log_class(c, True)
        att.log_class(c, False)
        self.assertEqual((c["held"], c["attended"]), (2, 1))

    def test_attended_more_than_held_rejected(self):
        with self.assertRaises(ValueError):
            mk(5, 6)


class TestCourses(unittest.TestCase):
    def test_duplicate_code(self):
        lst = []
        cm.add_course(lst, make_course("cs101", "Intro", 4))
        with self.assertRaises(ValueError):
            cm.add_course(lst, make_course("CS101", "Other", 3))
        self.assertEqual(len(lst), 1)

    def test_bad_values_rejected(self):
        with self.assertRaises(ValueError):
            make_course("", "Intro", 4)
        with self.assertRaises(ValueError):
            make_course("CS1", "Intro", 31)
        with self.assertRaises(ValueError):
            make_course("CS1", "Intro", 4, grade="Z")

    def test_edit_and_delete(self):
        lst = [make_course("CS101", "Intro", 4)]
        cm.edit_course(lst, "cs101", name="Basics", credits=3)
        self.assertEqual((lst[0]["name"], lst[0]["credits"]), ("Basics", 3))
        with self.assertRaises(ValueError):
            cm.edit_course(lst, "CS101", credits=99)
        self.assertEqual(lst[0]["credits"], 3)  # unchanged after failed edit
        self.assertTrue(cm.delete_course(lst, "CS101"))
        self.assertFalse(cm.delete_course(lst, "CS101"))


class TestStorage(unittest.TestCase):
    def test_corrupt_json_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "courses.json")
            with open(p, "w") as f:
                f.write("{ this is not json")
            self.assertEqual(storage.load_courses(p), [])
            self.assertTrue(os.path.exists(p + ".corrupt"))

    def test_missing_file_and_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "sub", "courses.json")
            self.assertEqual(storage.load_courses(p), [])
            original = [make_course("CS101", "Intro", 4, held=10, attended=8, grade="A")]
            storage.save_courses(original, p)
            self.assertEqual(storage.load_courses(p), original)
            leftovers = [f for f in os.listdir(os.path.dirname(p)) if f.endswith(".tmp")]
            self.assertEqual(leftovers, [])

    def test_bad_records_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "courses.json")
            with open(p, "w") as f:
                f.write('{"courses": [{"code": "A1", "name": "Ok", "credits": 3},'
                        ' {"code": "B2"}, 5, {"code": "C3", "name": "Bad", "credits": 99}]}')
            loaded = storage.load_courses(p)
            self.assertEqual([c["code"] for c in loaded], ["A1"])


if __name__ == "__main__":
    unittest.main()
