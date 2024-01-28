#!/usr/bin/env python3

import sys
import os
import yaml
import shlex
import subprocess
import ast
from multiprocessing import Pool

# sys.argv.pop() --> port
PORT = sys.argv.pop()

if not PORT:
    PORT = "esp32"

LOCAL_CI_PATH = os.getenv("LOCAL_CI_PATH", ".")
LOCAL_CI_PARALLEL = ast.literal_eval(os.getenv("LOCAL_CI_PARALLEL", "False"))
base_config = os.path.join(LOCAL_CI_PATH, f"{PORT}_boards.yaml")
config_file = os.getenv(f"{PORT}_BOARDS", base_config)


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
    result = subprocess.run(shlex.split(flash_cmd), stdout=stdout)
    return result


def test_board(port, board, board_config, stdout=sys.stdout):
    """
    $LOCAL_CI_PATH/device_test_runner.py $<PORT>_TEST_BOARD
    """
    test_cmd = f"{LOCAL_CI_PATH}/device_test_runner.py {port}:{board}"

    result = subprocess.run(shlex.split(test_cmd), stdout=stdout)
    return result


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
            return

        if board_config.get("TEST", False):
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


try:
    boards_config = load_board_config(config_file).get("boards", {})

except Exception as e:
    print(e)
    sys.exit(1)

if not LOCAL_CI_PARALLEL:
    if any(
        [board_runner(PORT, board, boards_config.get(board)) for board in boards_config]
    ):
        print("Done")
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
        p.starmap(board_runner, build_boards)
    print("Done")
