#!/usr/bin/env python3

import shlex
import sys
import os
import subprocess
import ast
import yaml

_TARGETS = {"stm32": "pyboard"}


LOCAL_CI_PATH = os.getenv("LOCAL_CI_PATH", ".")


def load_board_config(config):
    with open(config, "r") as cf:
        return yaml.safe_load(cf.read())


def get_test_target(target):
    return _TARGETS.get(target, target)


PORT = sys.argv.pop()

if ":" in PORT:
    PORT, BOARD = PORT.split(":")
else:
    BOARD = os.getenv(f"{PORT}_BOARD", "")


base_config = os.path.join(LOCAL_CI_PATH, f"{PORT}_boards.yaml")
config_file = os.getenv(f"{PORT}_BOARDS", base_config)

board_config = load_board_config(config_file).get("boards").get(BOARD, {})


DEVICE = board_config.get("PORT", os.getenv(f"{PORT.upper()}_DEVICE", "/dev/ttyUSB0"))

TEST_DEVICE = ast.literal_eval(os.getenv(f"{PORT.upper()}_TEST", "True"))

CMD_TESTS = shlex.split(
    f"./run-tests.py --target {get_test_target(PORT)} --device {DEVICE}"
)


if TEST_DEVICE:
    result = subprocess.run(CMD_TESTS, cwd="tests")
    sys.exit(result.returncode)
else:
    subprocess.run(["echo", "PORT:", PORT, "TESTS: [\u001b[33;1m SKIP\u001b[0m ]"])


# TODO: add run-multitest.py for devices ?
