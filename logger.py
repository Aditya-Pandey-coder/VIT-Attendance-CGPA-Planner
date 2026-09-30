# Sets up logging to logs/app.log
import logging
import os

import config

log = logging.getLogger("planner")
log.setLevel(logging.INFO)
log.propagate = False

if not log.handlers:
    try:
        os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
        handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    except OSError:
        handler = logging.NullHandler()  # can't write logs, just carry on
    log.addHandler(handler)
