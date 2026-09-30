# Saving and loading courses in a JSON file.
import json
import os
import tempfile

import config
from logger import log
from models import make_course


def load_courses(path=None):
    path = path or config.DATA_FILE
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        records = data["courses"] if isinstance(data, dict) else data
        if not isinstance(records, list):
            raise ValueError("courses is not a list")
    except (ValueError, KeyError, OSError) as err:  # JSONDecodeError is a ValueError
        log.error("Corrupt data file %s: %s", path, err)
        try:
            os.replace(path, path + ".corrupt")  # keep the bad file, start fresh
        except OSError:
            pass
        return []

    courses = []
    for r in records:
        try:
            courses.append(make_course(r["code"], r["name"], int(r["credits"]),
                                       int(r.get("semester", 1)),
                                       int(r.get("held", 0)),
                                       int(r.get("attended", 0)),
                                       r.get("grade")))
        except (KeyError, TypeError, ValueError, AttributeError) as err:
            log.warning("Skipping bad record %r: %s", r, err)
    log.info("Loaded %d course(s)", len(courses))
    return courses


def save_courses(courses, path=None):
    path = path or config.DATA_FILE
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)

    # write to a temp file first, then swap it in, so a crash can't ruin the data
    fd, temp_path = tempfile.mkstemp(dir=folder, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"courses": courses}, f, indent=2)
        os.replace(temp_path, path)
    except OSError:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        log.exception("Could not save %s", path)
        raise
    log.info("Saved %d course(s)", len(courses))
