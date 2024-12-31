from typing import List, Tuple
from bpy import ops
from bpy.types import Context, Operator
import bpy

from ..common import (do_git,
                      doc_saved, ui_refresh,
                      working_dir_clean,
                      check_repo_exists)
from .revisions import get_main_branch

branches_list = []
force_refresh = False


def list_branches(_self=None,
                  _context=None) -> List[Tuple[str, str, str]]:
    """Returns a list of branches to be passed to SelectBranch

    Returns:
        list: List of branches in the repository
    """
    global branches_list, force_refresh
    if branches_list and not force_refresh:
        return branches_list
    branches_list = []
    if check_repo_exists():
        current_branch = do_git(
            'rev-parse',
            '--abbrev-ref',
            'HEAD').rstrip()
        branches_list.append((current_branch, current_branch, ""))
        for branch in do_git("branch", "'--format=%(refname:short)'") \
                .splitlines():
            if not branch:
                break
            elif branch == current_branch:
                continue
            branches_list.append((branch, branch, ""))
    else:
        branches_list = [("", "No repo found", ""), ]

    return branches_list


class SwitchBranch(Operator):
    """Switch to a branch"""
    bl_idname = "blendgit.switch_branch"
    bl_label = "Switch Branch"

    def switch(self,
               context: Context,
               branch: str = ""):
        blendgit = context.window_manager.blendgit
        if not doc_saved():
            self.report({"ERROR"}, "Need to save first")
            return {"CANCELLED"}
        elif not working_dir_clean():
            self.report(
                {"ERROR"},
                "Working directory must be clean (try saving or stashing)")
            return {"CANCELLED"}

        if len(blendgit.branch_properties.branch) == 0:
            return {"CANCELLED"}

        if not branch:
            main_branch = get_main_branch()
            if not main_branch:
                self.report({"ERROR"}, "No main branch found!")
                return {"CANCELLED"}
            branch = main_branch
        do_git("checkout", branch)
        ops.wm.open_mainfile(
            "EXEC_DEFAULT", filepath=bpy.data.filepath)
        ui_refresh()
        self.report({"INFO"}, "Successfully switched branch!")

        return {"FINISHED"}

    def execute(self, context: Context):
        blendgit = context.window_manager.blendgit
        return self.switch(context, blendgit.branch_properties.branch)


class SwitchToMainBranch(SwitchBranch):
    """Switches to the main branch"""
    bl_idname = "blendgit.switch_to_main_branch"
    bl_label = "Switch to Main Branch"
    bl_description = "Switch to the project's main branch"

    def execute(self, context: Context):
        return self.switch(context)


registry = [
    SwitchBranch,
    SwitchToMainBranch,
]
