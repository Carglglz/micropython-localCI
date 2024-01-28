#!/usr/bin/env python3

import sys
import os
import yaml
import shlex
import subprocess
import ast
import time
import glob
from multiprocessing import Pool

# sys.argv.pop() --> port
PORT = sys.argv.pop()

if not PORT:
    PORT = "esp32"

LOCAL_CI_PATH = os.getenv("LOCAL_CI_PATH", ".")
LOCAL_CI_PARALLEL_BOARDS = ast.literal_eval(
    os.getenv("LOCAL_CI_PARALLEL_BOARDS", "False")
)
base_config = os.path.join(LOCAL_CI_PATH, os.path.join("config", f"{PORT}_boards.yaml"))
config_file = os.getenv(f"{PORT.upper()}_BOARDS_CONFIG", base_config)


def load_board_config(config):
    with open(config, "r") as cf:
        return yaml.safe_load(cf.read())


# <port>_boards.yaml
# boards:
#   PYBV11:
#       BOARD_DIR: "boards"
#       BUILD: true
#       FLASH: true
#       TEST: true
#
#       CUSTOM_TESTS: ''/ false
#       PORT: "/dev/ttyACM0"


def clean_board(port, board, board_config, stdout=sys.stdout):
    """
    make clean -C ports/{}  BOARD_DIR={}
    """

    _board_dir = board_config.get(
        "BOARD_DIR", os.getenv(f"{port.upper()}_BOARD_DIR", f"ports/{port}/boards")
    )
    board_dir = os.path.join(_board_dir, board)
    clean_cmd = f"make clean -C ports/{port} BOARD_DIR={board_dir}"

    result = subprocess.run(shlex.split(clean_cmd), stdout=stdout)
    return result


def build_board(port, board, board_config, stdout=sys.stdout):
    """
    make -C ports/{}  BOARD_DIR={} -j{}
    """
    _board_dir = board_config.get(
        "BOARD_DIR", os.getenv(f"{port.upper()}_BOARD_DIR", f"ports/{port}/boards")
    )
    board_dir = os.path.join(_board_dir, board)
    jobs = board_config.get("JOBS", 2)
    build_cmd = f"make -C ports/{port} BOARD_DIR={board_dir} -j{jobs}"

    result = subprocess.run(shlex.split(build_cmd), stdout=stdout)
    return result


def flash_board(port, board, board_config, stdout=sys.stdout):
    """
    make -C ports/{} BOAR_DIR={} PORT={} deploy
    """

    _board_dir = board_config.get(
        "BOARD_DIR", os.getenv(f"{port.upper()}_BOARD_DIR", f"ports/{port}/boards")
    )

    board_dir = os.path.join(_board_dir, board)
    bootloader_cmd = board_config.get("BOOTLOADER", "")
    device_port = board_config.get("PORT", "/dev/ttyUSB0")
    flash_cmd = f"make -C ports/{port} BOARD_DIR={board_dir} PORT={device_port} deploy"

    if bootloader_cmd:
        subprocess.run(shlex.split(bootloader_cmd), stdout=stdout)
        time.sleep(1)
    result = subprocess.run(shlex.split(flash_cmd), stdout=stdout)
    return result


def test_board(port, board, board_config, stdout=sys.stdout):
    """
    $LOCAL_CI_PATH/device_test_runner.py $<PORT>_TEST_BOARD
    """
    test_cmd = f"{LOCAL_CI_PATH}/device_test_runner.py {port}:{board}"
    time.sleep(2)
    result = subprocess.run(shlex.split(test_cmd), stdout=stdout)
    return result


def test_board_custom(port, board, board_config, stdout=sys.stdout):
    """
    $board_config/CUSTOM_TESTS

     CUSTOM_TESTS:
        HW_TEST:
         cmd: "pytest hw_tests"
         cwd: "<path_to_>/tests"
         env_path: "/home/cgg/.local/bin"
    """
    # device_port = board_config.get("PORT")

    time.sleep(2)
    custom_tests = board_config.get("CUSTOM_TESTS")
    results = {}
    if custom_tests:
        for test, params in custom_tests.items():
            test_cmd = params.get("cmd")
            cwd = params.get("cwd")
            # expand * files in cmd
            _test_cmd_split = []
            if "*" in test_cmd:
                for _cmd in shlex.split(test_cmd):
                    if "*" not in _cmd:
                        _test_cmd_split.append(_cmd)
                    else:
                        expand = glob.glob(os.path.join(cwd, _cmd))
                        _test_cmd_split += expand

            else:
                _test_cmd_split = shlex.split(test_cmd)

            env_path = {
                **os.environ,
                "PATH": f"{params.get('env_path')}:" + os.environ["PATH"],
            }

            # DEBUG:
            # print(test_cmd)
            # print(cwd)
            # print(env_path)
            results[test] = subprocess.run(
                _test_cmd_split, stdout=stdout, cwd=cwd, env=env_path
            )
    return results


def board_runner(
    port, board, board_config, parallel=False, stdout=sys.stdout, clean=True
):
    if parallel:
        subprocess.run(["echo", "PORT:", port, "BOARD:", board, "RUNNING"])
        with open(f"{port}_{board}.log", "w") as boardlog:
            return board_runner(port, board, board_config, stdout=boardlog, clean=False)
    else:
        if board_config.get("BUILD", False):
            if clean:
                result = clean_board(port, board, board_config, stdout=stdout)
            result = build_board(port, board, board_config, stdout=stdout)
            if result.returncode == 0:
                subprocess.run(
                    ["echo", "PORT:", port, "BOARD:", board, " BUILD [OK ]"],
                )
            else:
                subprocess.run(
                    ["echo", "PORT:", port, "BOARD:", board, " BUILD [ FAILED ]"]
                )
                return result.returncode
        else:
            subprocess.run(["echo", "PORT:", port, "BOARD:", board, " BUILD SKIP"])
            return

        if board_config.get("FLASH", False):
            result = flash_board(port, board, board_config, stdout=stdout)

            if result.returncode == 0:
                subprocess.run(
                    ["echo", "PORT:", port, "BOARD:", board, " FIRMWARE FLASH [ OK ]"]
                )
            else:
                subprocess.run(
                    [
                        "echo",
                        "PORT:",
                        port,
                        "BOARD:",
                        board,
                        " FIRMWARE FLASH [ FAILED ]",
                    ]
                )
                return result.returncode
        else:
            pass
            # return

        if board_config.get("TEST", False):
            subprocess.run(
                ["echo", "PORT:", port, "BOARD:", board, " Running tests..."]
            )
            result = test_board(port, board, board_config, stdout=stdout)

            if result.returncode == 0:
                subprocess.run(
                    ["echo", "PORT:", port, "BOARD:", board, " TESTS [ OK ]"]
                )
            else:
                subprocess.run(
                    ["echo", "PORT:", port, "BOARD:", board, " TESTS [ FAILED ]"]
                )
                return result.returncode

        if board_config.get("CUSTOM_TESTS", False):
            subprocess.run(
                ["echo", "PORT:", port, "BOARD:", board, " Running custom tests..."]
            )
            results = test_board_custom(port, board, board_config, stdout=stdout)

            if all([result.returncode == 0 for result in results.values()]):
                for test, result in results.items():
                    subprocess.run(
                        ["echo", "PORT:", port, "BOARD:", board, f"TEST: {test} [ OK ]"]
                    )
                return 0
            else:
                for test, result in results.items():
                    if result.returncode == 0:
                        subprocess.run(
                            [
                                "echo",
                                "PORT:",
                                port,
                                "BOARD:",
                                board,
                                f"TEST: {test} [ OK ]",
                            ]
                        )
                    else:
                        subprocess.run(
                            [
                                "echo",
                                "PORT:",
                                port,
                                "BOARD:",
                                board,
                                f" TEST: {test} [ FAILED ]",
                            ]
                        )
                return -1


try:
    boards_config = load_board_config(config_file).get("boards", {})

except Exception as e:
    print(e)
    sys.exit(1)

if not LOCAL_CI_PARALLEL_BOARDS:
    if not all(
        [board_runner(PORT, board, boards_config.get(board)) for board in boards_config]
    ):
        print("Done")
    else:
        sys.exit(-1)
else:
    print("Running mode: PARALLEL")
    print("redirecting output to <port>_<board>.log")
    build_boards = [
        (PORT, board, boards_config.get(board), True)
        for board in boards_config
        if boards_config.get(board).get("BUILD")
    ]
    for board in build_boards:
        clean_board(*board[:-1])
    with Pool(len(build_boards)) as p:
        result = p.starmap(board_runner, build_boards)
    if not all(result):
        print("Done")
    else:
        sys.exit(-1)
