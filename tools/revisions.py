from typing import List
import os

from bpy.props import StringProperty
from bpy.types import (Operator, Context, Event)
from bpy.ops import wm
import bpy

from ..common import (do_git,
                      working_dir_clean,
                      check_repo_exists,
                      ui_refresh,
                      git_log,
                      get_work_dir,)
from .lfs import initialize_lfs

revision_list = []
revision_list_needs_update = False
commits_list = []


# Loading


def get_main_branch() -> str:
    """Returns the main branch of the repo"""
    ensure_repo_exists()
    branches = do_git("branch").split('\n')
    branches = [branch.strip() for branch in branches]
    if 'main' in branches:
        return 'main'
    return 'master'


def which_branch() -> str:
    """Returns the current branch (if not in a commit)"""
    ensure_repo_exists()
    for line in do_git("branch").split("\n"):
        if "*" in line and "(" not in line:
            return line[2:].rstrip()
    return ""


# def list_commits(self=None, context=None):
#     """Generates the menu items showing the commit history for the user to
#     pick from."""
#     main_branch = get_main_branch()
#     current_branch = which_branch()
#     if not current_branch:
#         current_branch = main_branch
#     if check_repo_exists():
#         last_commits_list = []
#         for line in do_git(
#                 "log",
#                 "--format=%H %ct %s",
#                 "-n", "5",
#                 current_branch).split("\n"):
#             if not line:
#                 continue
#             commit_entry = line.split(" ", 2)
#             blender_list_entry = (
#                 commit_entry[0],  # Commit hash
#                 "%s: %s" % (format_compact_datetime(
#                     int(commit_entry[1])),  # Commit time
#                     commit_entry[2]),  # Commit description
#                 ""  # Blender expects something here
#             )
#             last_commits_list.append(blender_list_entry)
#     else:
#         last_commits_list = [("", "No repo found", ""), ]

#     return last_commits_list


# def get_commits(self=None, context=None) -> list:
#     """Gets the list of commits, initializing it if necessary"""
#     if not commits_list:
#         refresh_commit_list()
#     return commits_list


# def refresh_commit_list():
#     """Refreshes the list of commits"""
#     global commits_list
#     commits_list = list_commits()
#     ui_refresh()


# def refresh_commit_list_async():
#     """Refreshes the commit list asyncronously"""
#     thread = Thread(target=refresh_commit_list)
#     thread.start()


class LoadCommit(Operator):
    """Load a previous commit"""
    # FIXME: Untested
    bl_idname = "blendgit.load_commit"
    bl_label = "Load Commit"
    bl_description = "Load a commit from history"

    def execute(self, context: Context):
        blendgit = context.window_manager.blendgit
        revision_props = blendgit.revision_properties
        revision_list = revision_props.revision_list
        revision_list_index = revision_props.revision_list_index
        selected_revision = revision_list[revision_list_index]

        if not working_dir_clean():
            self.report({"ERROR"}, "Working directory not clean")
            return {"CANCELLED"}

        do_git("checkout", selected_revision["hash"])
        wm.open_mainfile(
            "EXEC_DEFAULT", filepath=bpy.data.filepath)  # type: ignore
        self.report({"INFO"}, "Successfully switched branch!")

        return {"FINISHED"}


# Saving


def add_files(file=None) -> bool:
    """Adds files to staging"""
    if file is None:
        do_git("add", "-A")
    else:
        do_git("add", file)

    ui_refresh()
    return True


def create_gitignore():
    with open("res/gitignore.template") as f:
        gitignore = f.read()
    work_dir = get_work_dir()
    gitignore_path = os.path.join(work_dir, '.gitignore')
    with open(gitignore_path, 'w', newline='\n') as f:
        f.write(gitignore)
    add_files('.gitignore')


def ensure_repo_exists():
    if not check_repo_exists():
        do_git("init")
        do_git("config", "--local", "core.autocrlf", "false")
        initialize_lfs()
        create_gitignore()


class StageFile(Operator):
    bl_idname = "blendgit.stage_file"
    bl_label = "Stage File"
    bl_description = "Stage a file"

    def execute(self, context: Context):
        blendgit = context.window_manager.blendgit
        file_props = blendgit.file_properties
        files_list: List[str] = file_props.files_list
        files_list_index: int = file_props.files_list_index
        file_to_stage: str = files_list[files_list_index].name

        ensure_repo_exists()
        add_files(file=file_to_stage)

        return {"FINISHED"}


class StageAll(Operator):
    bl_idname = "blendgit.stage_all"
    bl_label = "Stage All"
    bl_description = "Stage all files in project"

    def execute(self, context: Context):
        ensure_repo_exists()
        add_files()

        return {"FINISHED"}


class ResetStaged(Operator):
    bl_idname = "blendgit.reset_staged"
    bl_label = "Reset Staged"
    bl_description = "Reset all staged files in project"

    def execute(self, context: Context):
        do_git("reset", ".")

        return {"FINISHED"}


class SaveCommit(Operator):
    """Save and commit latest changes"""
    bl_idname = "blendgit.save_commit"
    bl_label = "Save Commit"
    bl_description = "Commit your changes"

    message: StringProperty(
        name="CommitMessage",
        description="Commit message")

    def execute(self, context: Context):
        blendgit = context.window_manager.blendgit
        revision_props = blendgit.revision_properties
        msg = revision_props.pending_commit_message

        if msg.strip():
            ensure_repo_exists()

            wm.save_as_mainfile(
                "EXEC_DEFAULT", filepath=bpy.data.filepath)  # type: ignore

            do_git("commit", "-m", msg)
            self.report({"INFO"}, "Success!")
            ui_refresh()
            result = {"FINISHED"}
        else:
            self.report({"ERROR"}, "Commit message cannot be empty")
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
    StageFile,
    StageAll,
    ResetStaged,
]
