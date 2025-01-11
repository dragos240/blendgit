from typing import List
import os

from bpy.props import StringProperty
from bpy.types import Operator, Context
from bpy.ops import wm
import bpy

from ..common import (do_git,
                      working_dir_clean,
                      check_repo_exists,
                      ui_refresh,
                      git_log,
                      get_work_dir,)
from .lfs import initialize_lfs


# Loading


def get_main_branch() -> str:
    """Returns the main branch of the repo"""
    ensure_repo_exists()
    for branch in do_git("branch").splitlines():
        if "main" in branch:
            return "main"
    return 'master'


def which_branch() -> str:
    """Returns the current branch (if not in a commit)"""
    ensure_repo_exists()
    ref = do_git("rev-parse", "--abbrev-ref", "HEAD").rstrip()
    if ref != get_main_branch():
        ref = do_git("rev-parse", "--short", "HEAD").rstrip()

    return ref


class LoadCommit(Operator):
    """Load a previous commit"""
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
        def has_staged_files() -> bool:
            files_list = blendgit.file_properties.files_list
            for file in files_list:
                if file["staged"]:
                    return True

            return False
        blendgit = context.window_manager.blendgit
        revision_props = blendgit.revision_properties
        msg = revision_props.pending_commit_message

        if not has_staged_files():
            self.report({"ERROR"}, "No files staged for commit")
            result = {"CANCELLED"}
        elif not msg.strip():
            self.report({"ERROR"}, "Commit message cannot be empty")
            result = {"CANCELLED"}
        else:
            ensure_repo_exists()

            wm.save_as_mainfile(
                "EXEC_DEFAULT", filepath=bpy.data.filepath)  # type: ignore

            do_git("commit", "-m", msg)
            self.report({"INFO"}, "Success!")
            ui_refresh()
            result = {"FINISHED"}

        return result

# Revisions


def refresh_revisions() -> List:
    return git_log()


registry = [
    LoadCommit,
    SaveCommit,
    StageFile,
    StageAll,
    ResetStaged,
]
