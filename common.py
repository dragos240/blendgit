from nt import listdir
import time
import os
import subprocess
import logging
from typing import Dict, List, Tuple
from shutil import which

import bpy


num_git_operations = 0


def log(*args):
    """Prints a message with level INFO"""
    logging.info(" ".join(args))


def doc_saved():
    """Checks if the current doc been saved at least once"""
    return len(bpy.data.filepath) != 0


def get_blendgit():
    blendgit = None
    if hasattr(bpy.data, "window_managers"):
        for windowManager in bpy.data.window_managers:
            blendgit = windowManager.blendgit
    if blendgit is None:
        raise Exception("Blendgit could not be initialized")

    return blendgit


def working_dir_clean(force_check: bool = False):
    """Checks if working dir is clean"""
    blendgit = get_blendgit()
    if blendgit.working_dir_is_clean is not None \
            and not force_check:
        return blendgit.working_dir_is_clean
    else:
        print("working_dir_is_clean is None")
        blendgit.working_dir_is_clean = not do_git("status",
                                                   "--porcelain")
        return blendgit.working_dir_is_clean


def has_git() -> bool:
    """Checks if Git is installed"""
    blendgit = get_blendgit()
    if "git_installed" in blendgit.git_checks_done:
        return blendgit.git_checks_done["git_installed"]
    blendgit.git_checks_done["git_installed"] = False
    if which("git") is not None:
        blendgit.git_checks_done["git_installed"] = True
        return True
    return False


def check_repo_exists() -> bool:
    if os.path.exists(os.path.join(get_work_dir(), ".git")):
        return True
    return False


def get_work_dir():
    """Gets work directory"""
    path = os.path.split(bpy.data.filepath)[0]
    for _ in range(3):
        for file in listdir(path):
            if file.startswith(".git"):
                return path
        path = os.path.join(path, "..")

    raise Exception()


def needs_refresh(refresh_type: str) -> bool:
    blendgit = get_blendgit()
    if refresh_type == "revisions" \
            and blendgit.num_revision_list_refreshes != get_num_operations():
        return True
    elif refresh_type == "files" \
            and blendgit.num_file_list_refreshes != get_num_operations():
        return True

    return False


@bpy.app.handlers.persistent
def ui_refresh_for_handler(dummy1: bpy.types.Scene, dummy2):
    """Necessary for ui_refresh to be called when file is reloaded"""
    ui_refresh()


def ui_refresh():
    """Refreshes all UI elements"""
    # Logic taken from CATS plugin
    # (https://github.com/absolute-quantum/cats-blender-plugin)
    refreshed = False
    while not refreshed:
        if hasattr(bpy.data, 'window_managers'):
            for windowManager in bpy.data.window_managers:
                # Check if working directory is clean on ui refresh
                if hasattr(windowManager, "blendgit"):
                    blendgit = windowManager.blendgit
                    blendgit.working_dir_is_clean = working_dir_clean(
                        force_check=True)
                # Redraw areas
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
    lines = do_git(
        "log", "--pretty=format:%h%x09%cs%x09%s", "-n", "5").splitlines()
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
        " ": ""
    }

    def get_statuses_from_code(code: str) -> Tuple[str, str]:
        staged_status = code[0]
        working_status = code[1]
        try:
            if "?" in staged_status:
                staged_status = ""
                working_status = "new"
            else:
                staged_status = STATUS_TYPE[staged_status]
                working_status = STATUS_TYPE[working_status]
        except KeyError:
            pass

        return (staged_status, working_status)

    def parse_line(line: str) -> Dict:
        parts = [line[:2], " ".join(line[2:].split())]
        staged_status, working_status = get_statuses_from_code(parts[0])
        entry = {
            "status": (staged_status
                       if staged_status.rstrip()
                       else working_status),
            "file_path": parts[1].replace('"', ''),
            "staged": (True
                       if (staged_status.rstrip())
                       else False)
        }
        return entry

    entries = []
    lines = do_git("status", "--porcelain=1").splitlines()
    for line in lines:
        entry = parse_line(line)

        entries.append(entry)

    return entries


def do_git(*args) -> str:
    """Common routine for invoking various Git functions."""
    global num_git_operations
    env = dict(os.environ)
    work_dir = get_work_dir()
    env["GIT_DIR"] = ".git"

    # Make sure all args are strings
    args = [str(arg) for arg in args]
    # We need to make this into a string since shell==True
    cmd = "git " + " ".join(args)
    print(cmd)

    try:
        result = subprocess.run(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=work_dir,
            env=env,
            check=True,
        )
        output = result.stdout.decode('utf-8').rstrip()

        if args[0] not in ("status", "log"):
            num_git_operations += 1
        return output
    except subprocess.CalledProcessError as e:
        print("git encountered an error:")
        print(f"  stdout: {e.stdout}")
        print(f"  stdout: {e.stderr}")
        raise e


def get_num_operations() -> int:
    return num_git_operations
