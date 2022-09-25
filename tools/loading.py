from threading import Thread

import time

import bpy

from ..common import (do_git,
                      working_dir_clean,
                      check_repo_exists,
                      stash_save,
                      ui_refresh)

commits_list = []


def format_compact_datetime(timestamp: int) -> str:
    """Returns as brief as possible a human-readable display of the specified
    date/time."""
    then_items = time.localtime(timestamp)
    now = time.time()
    now_items = time.localtime(now)
    if abs(now - timestamp) < 86400:
        format = "%H:%M:%S"
    else:
        format = "%b-%d %H:%M"
        if then_items.tm_year != now_items.tm_year:
            format = "%Y " + format

    return \
        time.strftime(format, then_items)


def get_main_branch() -> str:
    """Returns the main branch of the repo"""
    if not check_repo_exists():
        return None
    branches = do_git("branch").split('\n')
    branches = [branch.strip() for branch in branches]
    if 'main' in branches:
        return 'main'
    return 'master'


def which_branch() -> str:
    """Returns the current branch (if not in a commit)"""
    branch = None
    if not check_repo_exists():
        return None
    for line in do_git("branch").split("\n"):
        if "*" in line and "(" not in line:
            branch = line[2:].rstrip()
            break

    return branch


def list_commits(self=None, context=None):
    """Generates the menu items showing the commit history for the user to
    pick from."""
    last_commits_list = []
    main_branch = get_main_branch()
    current_branch = which_branch()
    if current_branch is None:
        current_branch = main_branch
    if check_repo_exists():
        # Blender bug? Items in menu end up in reverse order from that in
        # my list
        last_commits_list = []
        for line in do_git(
                "log",
                "--format=%H %ct %s",
                "-n", "5",
                current_branch).split("\n"):
            if not line:
                continue
            for commit_entry in (line.split(" ", 2),):
                blender_list_entry = (
                    commit_entry[0],  # Commit hash
                    "%s: %s" % (format_compact_datetime(
                        int(commit_entry[1])),  # Commit time
                        commit_entry[2]),  # Commit description
                    ""  # Blender expects something here
                )
                last_commits_list.append(blender_list_entry)
    else:
        last_commits_list = [("", "No repo found", ""), ]

    return last_commits_list


def get_commits(self=None, context=None) -> list:
    """Gets the list of commits, initializing it if necessary"""
    refresh_commit_list()
    return commits_list


def refresh_commit_list():
    """Refreshes the list of commits"""
    global commits_list
    commits_list = list_commits()
    ui_refresh()


def refresh_commit_list_async():
    """Refreshes the commit list asyncronously"""
    thread = Thread(target=refresh_commit_list)
    thread.start()


class LoadCommit(bpy.types.Operator):
    """Load a previous commit"""
    bl_idname = "blendgit.load_commit"
    bl_label = "Load Commit"

    def execute(self, context: bpy.types.Context):
        if context.window_manager.versions.stash \
                and context.window_manager.versions.stash_message:
            print("Doing stash for",
                  context.window_manager.versions.stash_message)
            stash_save(context.window_manager.versions.stash_message,
                       background=False)
        elif context.window_manager.versions.stash \
                and not context.window_manager.versions.stash_message:
            self.report({"ERROR"}, "Please enter a stash message")
            return {"CANCELLED"}
        if len(context.window_manager.versions.commit) != 0:
            if not working_dir_clean():
                self.report({"ERROR"}, "Working directory not clean")
                return {"CANCELLED"}
            do_git("checkout", context.window_manager.versions.commit)
            bpy.ops.wm.open_mainfile(
                "EXEC_DEFAULT", filepath=bpy.data.filepath)
            result = {"FINISHED"}
        else:
            result = {"CANCELLED"}

        return result


registry = [
    LoadCommit,
]
