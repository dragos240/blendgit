from typing import List
import time
from threading import Thread
import os

from bpy.props import StringProperty
from bpy.types import (Operator, Context)
from bpy.ops import wm
from bpy import data

from ..common import (do_git,
                      working_dir_clean,
                      check_repo_exists,
                      ui_refresh,
                      git_log,
                      get_work_dir,)
from .stash import stash_save
from .lfs import initialize_lfs

revision_list = []
revision_list_needs_update = False
commits_list = []


# Loading


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
        return ""
    branches = do_git("branch").split('\n')
    branches = [branch.strip() for branch in branches]
    if 'main' in branches:
        return 'main'
    return 'master'


def which_branch() -> str:
    """Returns the current branch (if not in a commit)"""
    if not check_repo_exists():
        return ""
    for line in do_git("branch").split("\n"):
        if "*" in line and "(" not in line:
            return line[2:].rstrip()
    return ""


def list_commits(self=None, context=None):
    """Generates the menu items showing the commit history for the user to
    pick from."""
    main_branch = get_main_branch()
    current_branch = which_branch()
    if not current_branch:
        current_branch = main_branch
    if check_repo_exists():
        last_commits_list = []
        for line in do_git(
                "log",
                "--format=%H %ct %s",
                "-n", "5",
                current_branch).split("\n"):
            if not line:
                continue
            commit_entry = line.split(" ", 2)
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
    if not commits_list:
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


class LoadCommit(Operator):
    """Load a previous commit"""
    bl_idname = "blendgit.load_commit"
    bl_label = "Load Commit"

    def execute(self, context: Context):
        versions = context.window_manager.blendgit.versions
        stash_message = versions.stash_message if versions.stash else None

        if versions.stash:
            if stash_message:
                print("Doing stash for", stash_message)
                stash_save(stash_message, background=False)
            else:
                self.report({"ERROR"}, "Please enter a stash message")
                return {"CANCELLED"}

        if versions.commit:
            if not working_dir_clean():
                self.report({"ERROR"}, "Working directory not clean")
                return {"CANCELLED"}
            do_git("checkout", versions.commit)
            wm.open_mainfile(
                "EXEC_DEFAULT", filepath=data.filepath)  # type: ignore
            return {"FINISHED"}

        return {"CANCELLED"}


# Saving


def add_files(add_type=None, file=None) -> bool:
    """Adds files to staging"""
    if add_type not in ('all', 'category') and file is None:
        print("Type must be one of all/category, "
              + "or 'file' param must be set")
        return False
    if add_type == 'all':
        do_git("add", "-A")
    elif add_type == 'category':
        for category, match, mismatch in (
                ("fonts", {}, (("filepath", "<builtin>"),)),
                ("images", {"type": "IMAGE"}, ()),
                ("libraries", {}, ()),
                ("sounds", {}, ())):
            for item in getattr(data, category):
                # not packed into .blend file
                if (item.packed_file is None
                    # must be relative to .blend file
                    and item.filepath.startswith("//")
                    # must not be at higher level than .blend file
                    and not item.filepath.startswith("//..")
                    # make sure there is no mismatch
                        and not any(getattr(item, k) == v
                                    for k, v in mismatch)
                    # make sure item has all match attributes
                    and all(getattr(item, k) == match[k]
                            for k in match)):
                    # We know the file is relative, remove prefix
                    relative_path = item.filepath[2:]
                    add_files(file=relative_path)
    elif file is not None:
        do_git("add", "--", file)
    return True


def create_gitignore():
    with open("res/gitignore.template") as f:
        gitignore = f.read()
    work_dir = get_work_dir()
    gitignore_path = os.path.join(work_dir, '.gitignore')
    with open(gitignore_path, 'w', newline='\n') as f:
        f.write(gitignore)
    do_git("add", '.gitignore')


class SaveCommit(Operator):
    """Save and commit latest changes"""
    bl_idname = "blendgit.save_commit"
    bl_label = "Save Commit"

    message: StringProperty(
        name="CommitMessage",
        description="Commit message")

    def execute(self, context: Context):
        msg = context.window_manager.blendgit.versions.commit_message

        if msg.strip():
            if not check_repo_exists():
                do_git("init")
                do_git("config", "--local", "core.autocrlf", "false")
                initialize_lfs()
                create_gitignore()

            wm.save_as_mainfile(
                "EXEC_DEFAULT", filepath=data.filepath)
            add_files(file=os.path.basename(data.filepath))
            add_files(add_type='category')

            do_git("commit", "-am", msg)
            self.report({"INFO"}, "Success!")
            refresh_commit_list_async()
            result = {"FINISHED"}
        else:
            self.report({"ERROR"}, "Comment cannot be empty")
            result = {"CANCELLED"}

        return result

# Revisions


def refresh_revisions() -> List:
    global revision_list, revision_list_needs_update

    if not revision_list or revision_list_needs_update:
        revision_list = git_log()
        revision_list_needs_update = False

    return revision_list


def set_revision_list_need_update():
    global revision_list_needs_update
    revision_list_needs_update = True


registry = [
    LoadCommit,
    SaveCommit,
]
