import time
import os
import subprocess
import logging
from typing import Dict, List

import bpy


def log(*args):
    """Prints a message with level INFO"""
    logging.info(" ".join(args))


def doc_saved():
    """Checks if the current doc been saved at least once"""
    return len(bpy.data.filepath) != 0


def working_dir_clean():
    """Checks if working dir is clean"""
    return not do_git("status",
                      "--porcelain",
                      "--untracked-files=no").rstrip()


def check_repo_exists():
    if os.path.exists(os.path.join(get_work_dir(), ".git")):
        return True
    return False


def get_work_dir():
    """Gets work directory"""
    return os.path.split(bpy.data.filepath)[0]


def ui_refresh():
    """Refreshes all UI elements"""
    # Logic taken from CATS plugin
    # (https://github.com/absolute-quantum/cats-blender-plugin)
    refreshed = False
    while not refreshed:
        if hasattr(bpy.data, 'window_managers'):
            for windowManager in bpy.data.window_managers:
                for window in windowManager.windows:
                    for area in window.screen.areas:
                        area.tag_redraw()
            refreshed = True
            print('Refreshed UI')
        else:
            time.sleep(0.1)


def git_log() -> List[Dict[str, str]]:
    def parse_line(line: str) -> Dict:
        parts = line.split("\t")
        return {
            "hash": parts[0],
            "date": parts[1],
            "message": parts[2],
        }

    entries = []
    lines = do_git("log", "--pretty=format:%h%x09%cs%x09%s").splitlines()
    for line in lines:
        entry = parse_line(line)

        entries.append(entry)

    return entries


def status() -> List[Dict[str, str]]:
    STATUS_TYPE = {
        "M": "modified",
        "A": "added",
        "D": "deleted",
        "R": "renamed",
        "?": "new",
    }

    def get_status_from_code(code: str) -> str:
        # We don't care about the index, so only working dir changes
        try:
            working_status = STATUS_TYPE[code[1]]
        except KeyError:
            working_status = code

        return working_status

    def parse_line(line: str) -> Dict:
        parts = [line[:2], line.split()[-1]]
        return {
            "status": get_status_from_code(parts[0]),
            "file_path": parts[-1]
        }

    entries = []
    lines = do_git("status", "--porcelain=1").splitlines()
    for line in lines:
        entry = parse_line(line)

        entries.append(entry)

    return entries


def do_git(*args):
    """Common routine for invoking various Git functions."""
    env = dict(os.environ)
    work_dir = get_work_dir()
    env["GIT_DIR"] = ".git"

    return \
        subprocess.check_output(
            args=("git", *args),
            stdin=subprocess.DEVNULL,
            shell=False,
            cwd=work_dir,
            env=env
        ).decode('utf-8').rstrip()
