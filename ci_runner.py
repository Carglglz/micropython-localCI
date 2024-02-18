#!/usr/bin/env python3
import subprocess
import shlex
import os
from multiprocessing import Pool
import ast


OK = "\033[92;1mOK\x1b[0m"
FAILED = "\u001b[31;1mFAILED\u001b[0m"
RUNNING = "\u001b[32;1mRUNNING\u001b[0m"

LOCAL_CI_PATH = os.getenv("LOCAL_CI_PATH", ".")
LOCAL_CI_PORTS = os.getenv("LOCAL_CI_PORTS", "all")
LOCAL_CI_PARALLEL = ast.literal_eval(os.getenv("LOCAL_CI_PARALLEL", "False"))

_run_ci = False

updated_paths = subprocess.check_output(
    shlex.split("git diff master... --name-only")
).decode()

print("UPDATED_PATHS:", f"\n{updated_paths}", flush=True)

UPDATED_PATHS = updated_paths.splitlines()

PORTS = ["unix", "esp32", "stm32", "rp2"]

COMMON_PATHS = ["py", "extmod", "lib", "tests"]

MPY_CROSS = "make -C mpy-cross"


def check_updated_paths(port):
    port_dir = os.path.join("ports", port)
    if any([port_dir in path for path in UPDATED_PATHS]) and (
        (port in LOCAL_CI_PORTS) or LOCAL_CI_PORTS == "all"
    ):
        return True

    if any(
        [
            any([path.startswith(cpath) for path in UPDATED_PATHS])
            and ((port in LOCAL_CI_PORTS) or LOCAL_CI_PORTS == "all")
            for cpath in COMMON_PATHS
        ]
    ):
        return True


def run_port_ci(port):
    # TODO: evaluate result: OK/FAIL
    if check_updated_paths(port):
        _ci_port_runner = os.path.join(LOCAL_CI_PATH, f"local_ci_{port}.sh")
        if os.path.exists(_ci_port_runner):
            if LOCAL_CI_PARALLEL:
                print("PORT:", port, f"[ {RUNNING} ]", flush=True)
                with open(f"{port}.log", "w") as portlog:
                    result = subprocess.run(_ci_port_runner, stdout=portlog)
                # TODO: parse <port.log> grep and evaluate result
            else:
                result = subprocess.run(_ci_port_runner)

            if result.returncode == 0:
                print("PORT:", port, f"[ {OK} ]", flush=True)
            else:
                print("PORT:", port, f"[ {FAILED} ]", flush=True)
            # TODO: add port callbacks? --> e.g. notify
            return result.returncode
        else:
            print("PORT:", port, "[\u001b[33;1m SKIP\u001b[0m ]", flush=True)

    else:
        print("PORT:", port, "[\u001b[33;1m SKIP\u001b[0m ]", flush=True)


# Trigger the appropriate local_ci_xx.sh runner
_run_ci = any([check_updated_paths(port) for port in PORTS])

if _run_ci:
    subprocess.run(shlex.split(MPY_CROSS))
    if not LOCAL_CI_PARALLEL:
        if any([run_port_ci(port) for port in PORTS]):
            print("Done")
    else:
        # TODO: run git submodule with lock
        print("Running mode: PARALLEL")
        print("redirecting output to <port>.log")
        with Pool(len(PORTS)) as p:
            p.map(run_port_ci, PORTS)
        print("Done")
else:
    print("Nothing to build/test")
