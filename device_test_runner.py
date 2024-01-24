#!/usr/bin/env python3

import shlex
import sys
import os
import subprocess
import ast

_TARGETS = {"stm32": "pyboard"}


def get_test_target(target):
    return _TARGETS.get(target, target)


TARGET = sys.argv.pop()

DEVICE = os.getenv(f"{TARGET.upper()}_DEVICE", "/dev/ttyUSB0")

TEST_DEVICE = ast.literal_eval(os.getenv(f"{TARGET.upper()}_TEST", "True"))

CMD_TESTS = shlex.split(f"./run-tests.py --target {get_test_target(TARGET)} --device {DEVICE}")

if TEST_DEVICE:
    result = subprocess.run(CMD_TESTS, cwd="tests")
    sys.exit(result.returncode)
else:
    subprocess.run(["echo", "PORT:", TARGET, "TESTS: SKIP"])

# TODO: add run-multitest.py for devices


# run other tests depending on device or custom tests
