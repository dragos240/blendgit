import time
import os
import subprocess
import logging
from threading import Thread

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


def stash_save(msg, background=True):
    def stash():
        if not check_repo_exists():
            return
        do_git("stash", "save", "-u", msg)
    if not background:
        stash()
        return
    thread = Thread(target=stash)
    thread.start()


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
        ).decode('utf-8').strip()
