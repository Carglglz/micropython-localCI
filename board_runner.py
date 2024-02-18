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
import argparse

parser = argparse.ArgumentParser(prog="board_runner.py", description="Board Runner")
parser.add_argument(
    "port", help="name of the port", choices=["unix", "esp32", "stm32", "rp2"]
)

parser.add_argument(
    "--boards",
    default="boards",
    help="boards key in <port>_boards.yaml config file",
)

args = parser.parse_args()


# fall back to a defined <PORT>_BOARD_GROUP in .env file as default
# but allow override it with --boards arg
parser.add_argument(
    "--boardgroup",
    default=(
        args.boards
        if args.boards != "boards"
        else os.getenv(f"{args.port.upper()}_BOARD_GROUP", args.boards)
    ),
    help="boards key in <port>_boards.yaml config file",
)

args = parser.parse_args()

args.boards = args.boardgroup


OK = "\033[92mOK\x1b[0m"
FAILED = "\u001b[31;1mFAILED\u001b[0m"
RUNNING = "\u001b[32;1mRUNNING\u001b[0m"
PORT = args.port

if not PORT:
    PORT = "esp32"

LOCAL_CI_PATH = os.getenv("LOCAL_CI_PATH", ".")
LOCAL_CI_PARALLEL_BOARDS = ast.literal_eval(
    os.getenv("LOCAL_CI_PARALLEL_BOARDS", "False")
)
base_config = os.path.join(LOCAL_CI_PATH, os.path.join("config", f"{PORT}_boards.yaml"))
config_file = os.getenv(f"{PORT.upper()}_BOARDS_CONFIG", base_config)


def replace_env_var(str_path):
    if not str_path:
        return
    if "$PWD" in str_path:
        return str_path.replace("$PWD", os.environ.get("PWD", os.getcwd()))
    elif "$LOCAL_CI_PATH" in str_path:
        return str_path.replace(
            "$LOCAL_CI_PATH", os.environ.get("LOCAL_CI_PATH", os.getcwd())
        )
    else:
        return str_path


def load_board_config(config):
    """

    boards:
     PYBV11:
         BUILD: true
         FLASH: true
         TEST: true # ./run-tests.py
         JOBS: 10
         PORT: "/dev/ttyACM0"
         BOOTLOADER: "tools/mpremote/mpremote.py bootloader"
         CUSTOM_TESTS:

            TEST_HW:
             test_dir: "$PWD/tests/ports/stm32"
             test_files: "*.py"
             cmd: "./run-tests.py $test_dir/$test_files --target pyboard --device /dev/ttyACM0 "
             cwd: "./tests"
             env_path: ""

            RESET:
             cmd: "./tools/mpremote/mpremote.py a0 reset"
    """
    with open(config, "r") as cf:
        return yaml.safe_load(cf.read())


def clean_board(port, board, board_config, stdout=sys.stdout):
    """
    make clean -C ports/{}  BOARD_DIR={}
    """

    _board_dir = board_config.get(
        "BOARD_DIR",
        os.getenv(
            f"{port.upper()}_BOARD_DIR", replace_env_var(f"$PWD/ports/{port}/boards")
        ),
    )
    board_dir = os.path.join(_board_dir, board)
    clean_cmd = f"make clean -C ports/{port} BOARD_DIR={board_dir}"

    clean_opt = board_config.get("CLEAN", True)

    if clean_opt:
        result = subprocess.run(shlex.split(clean_cmd), stdout=stdout)
    else:
        result = 0
        print(
            "PORT:",
            port,
            "BOARD:",
            board,
            " CLEAN [\u001b[33;1m SKIP\u001b[0m ]",
            flush=True,
        )

    return result


def build_board(port, board, board_config, stdout=sys.stdout):
    """
    make -C ports/{}  BOARD_DIR={} -j{}
    """
    _board_dir = board_config.get(
        "BOARD_DIR",
        os.getenv(
            f"{port.upper()}_BOARD_DIR", replace_env_var(f"$PWD/ports/{port}/boards")
        ),
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
        "BOARD_DIR",
        os.getenv(
            f"{port.upper()}_BOARD_DIR", replace_env_var(f"$PWD/ports/{port}/boards")
        ),
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
         test_dir:
         test_files:
         cmd: "pytest hw_tests"
         cwd: "<path_to_>/tests"
         env_path: ""
    """
    time.sleep(2)
    custom_tests = board_config.get("CUSTOM_TESTS")
    results = {}
    if custom_tests:
        for test, params in custom_tests.items():
            test_cmd = params.get("cmd")
            cwd = params.get("cwd", ".")
            if "$test_dir" in test_cmd:
                test_cmd = test_cmd.replace(
                    "$test_dir", replace_env_var(params.get("test_dir"))
                )
            if "$test_files" in test_cmd:
                test_cmd = test_cmd.replace("$test_files", params.get("test_files"))
            if "$PORT" in test_cmd:
                test_cmd = test_cmd.replace("$PORT", board_config.get("PORT", ""))
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

            env_path = os.environ

            if params.get("env_path"):
                env_path = {
                    **os.environ,
                    "PATH": f"{params.get('env_path')}:" + os.environ["PATH"],
                }

            # DEBUG:
            # print(test_cmd)
            # print(cwd)
            # print(env_path)
            time.sleep(int(params.get("sleep", "0")))
            results[test] = subprocess.run(
                _test_cmd_split, stdout=stdout, cwd=cwd, env=env_path
            )
    return results


def board_runner(
    port, board, board_config, parallel=False, stdout=sys.stdout, clean=True
):
    if parallel:
        print(*["PORT:", port, "BOARD:", board, f"[ {RUNNING} ]"])
        with open(f"{port}_{board}.log", "w") as boardlog:
            return board_runner(port, board, board_config, stdout=boardlog, clean=False)
    else:
        if board_config.get("BUILD", False):
            if clean:
                result = clean_board(port, board, board_config, stdout=stdout)
            result = build_board(port, board, board_config, stdout=stdout)
            if result.returncode == 0:
                print("PORT:", port, "BOARD:", board, f" BUILD [ {OK} ]", flush=True)
            else:
                print(
                    "PORT:", port, "BOARD:", board, f" BUILD [ {FAILED} ]", flush=True
                )

                if board_config.get("CALLBACKS", False):
                    callback = board_config.get("CALLBACKS").get("on_error", {})

                    # cb_results = []
                    if len(callback) == 1:
                        cmd = replace_env_var(callback.get("cmd"))
                        subprocess.run(shlex.split(cmd))
                    elif len(callback) > 1:
                        for cb in callback:
                            cmd = replace_env_var(callback.get(cb).get("cmd"))
                            subprocess.run(shlex.split(cmd))

                return result.returncode
        else:
            print(
                "PORT:",
                port,
                "BOARD:",
                board,
                " BUILD [\u001b[33;1m SKIP\u001b[0m ]",
                flush=True,
            )
            if not board_config.get("CUSTOM_TESTS"):
                return

        if board_config.get("FLASH", False):
            result = flash_board(port, board, board_config, stdout=stdout)

            if result.returncode == 0:
                print(
                    "PORT:",
                    port,
                    "BOARD:",
                    board,
                    f" FIRMWARE FLASH [ {OK} ]",
                    flush=True,
                )
            else:
                print(
                    "PORT:",
                    port,
                    "BOARD:",
                    board,
                    f" FIRMWARE FLASH [ {FAILED} ]",
                    flush=True,
                )

                if board_config.get("CALLBACKS", False):
                    callback = board_config.get("CALLBACKS").get("on_error", {})

                    # cb_results = []
                    if len(callback) == 1:
                        cmd = replace_env_var(callback.get("cmd"))
                        subprocess.run(shlex.split(cmd))
                    elif len(callback) > 1:
                        for cb in callback:
                            cmd = replace_env_var(callback.get(cb).get("cmd"))
                            subprocess.run(shlex.split(cmd))
                return result.returncode
        else:
            pass
            # return

        if board_config.get("TEST", False):
            print("PORT:", port, "BOARD:", board, " Running tests...", flush=True)
            result = test_board(port, board, board_config, stdout=stdout)

            if result.returncode == 0:
                print("PORT:", port, "BOARD:", board, f" TESTS [ {OK} ]", flush=True)
            else:
                print(
                    "PORT:", port, "BOARD:", board, f" TESTS [ {FAILED} ]", flush=True
                )

                if board_config.get("CALLBACKS", False):
                    callback = board_config.get("CALLBACKS").get("on_error", {})

                    # cb_results = []
                    if len(callback) == 1:
                        cmd = replace_env_var(callback.get("cmd"))
                        subprocess.run(shlex.split(cmd))
                    elif len(callback) > 1:
                        for cb in callback:
                            cmd = replace_env_var(callback.get(cb).get("cmd"))
                            subprocess.run(shlex.split(cmd))
                return result.returncode

        if board_config.get("CUSTOM_TESTS", False):
            print(
                "PORT:", port, "BOARD:", board, " Running custom tests...", flush=True
            )
            results = test_board_custom(port, board, board_config, stdout=stdout)
            _failed_tests = []

            if all([result.returncode == 0 for result in results.values()]):
                for test, result in results.items():
                    print(
                        "PORT:",
                        port,
                        "BOARD:",
                        board,
                        f"TEST: {test} [ {OK} ]",
                        flush=True,
                    )
                if board_config.get("CALLBACKS", False):
                    callback = board_config.get("CALLBACKS").get("on_success", {})

                    # cb_results = []

                    if len(callback) == 1:
                        cmd = replace_env_var(callback.get("cmd"))
                        subprocess.run(shlex.split(cmd))
                    elif len(callback) > 1:
                        for cb in callback:
                            cmd = replace_env_var(callback.get(cb).get("cmd"))
                            subprocess.run(shlex.split(cmd))

                return 0
            else:
                for test, result in results.items():
                    if result.returncode == 0:
                        print(
                            "PORT:",
                            port,
                            "BOARD:",
                            board,
                            f"TEST: {test} [ {OK} ]",
                            flush=True,
                        )
                    else:
                        _failed_tests.append(test)
                        print(
                            "PORT:",
                            port,
                            "BOARD:",
                            board,
                            f"TEST: {test} [ {FAILED} ]",
                            flush=True,
                        )

                print(
                    "PORT:",
                    port,
                    "BOARD:",
                    board,
                    f"TEST: {len(_failed_tests)} [ {FAILED} ]: ",
                    ", ".join(_failed_tests),
                    flush=True,
                )

                if board_config.get("CALLBACKS", False):
                    callback = board_config.get("CALLBACKS").get("on_error", {})

                    # cb_results = []

                    if len(callback) == 1:
                        cmd = replace_env_var(callback.get("cmd"))
                        subprocess.run(shlex.split(cmd))
                    elif len(callback) > 1:
                        for cb in callback:
                            cmd = replace_env_var(callback.get(cb).get("cmd"))
                            subprocess.run(shlex.split(cmd))

                return -1

        if board_config.get("CALLBACKS", False):
            callbacks = board_config.get("CALLBACKS")

            # cb_results = []
            for cb in callbacks:
                cmd = replace_env_var(callbacks[cb].get("cmd"))
                subprocess.run(shlex.split(cmd))

        return 0


try:
    boards_config = load_board_config(config_file).get(args.boards, {})

    print(*["PORT:", PORT, "BOARDS:", f"[{args.boards}]"])
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
