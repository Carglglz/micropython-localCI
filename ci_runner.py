#!/usr/bin/env python3
import subprocess
import shlex
import os
from multiprocessing import Pool
import ast

LOCAL_CI_PATH = os.getenv("LOCAL_CI_PATH", "tools/local_ci")
LOCAL_CI_PORTS = os.getenv("LOCAL_CI_PORTS", "all")
LOCAL_CI_PARALLEL = ast.literal_eval(os.getenv("LOCAL_CI_PARALLEL", "False"))

_run_ci = False

updated_paths = subprocess.check_output(shlex.split("git diff master... --name-only")).decode()

subprocess.run(["echo", "UPDATED_PATHS:", f"\n{updated_paths}"])

UPDATED_PATHS = updated_paths.splitlines()

PORTS = ["unix", "esp32", "stm32", "rp2"]

COMMON_PATHS = ["py", "extmod", "lib"]


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
                subprocess.run(["echo", "PORT:", port, "RUNNING"])
                with open(f"{port}.log", "w") as portlog:
                    result = subprocess.run(_ci_port_runner, stdout=portlog)
                # TODO: parse <port.log> grep and evaluate result
            else:
                result = subprocess.run(_ci_port_runner)

            if result.returncode == 0:
                subprocess.run(["echo", "PORT:", port, "[ OK ]"])
            else:
                subprocess.run(["echo", "PORT:", port, "[ FAILED ]"])
            return result.returncode
        else:
            subprocess.run(["echo", "PORT:", port, "SKIP"])

    else:
        subprocess.run(["echo", "PORT:", port, "SKIP"])


# Trigger the appropriate local_ci_xx.sh runner
_run_ci = any([check_updated_paths(port) for port in PORTS])

if _run_ci:
    if not LOCAL_CI_PARALLEL:
        if any([run_port_ci(port) for port in PORTS]):
            print("Done")
    else:
        print("Running mode: PARALLEL")
        print("redirecting output to <port>.log")
        with Pool(len(PORTS)) as p:
            p.map(run_port_ci, PORTS)
        print("Done")
else:
    print("Nothing to build/test")
