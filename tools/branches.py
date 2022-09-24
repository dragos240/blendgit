import bpy

from ..common import (do_git,
                      doc_saved,
                      working_dir_clean,
                      check_repo_exists,
                      stash_save)


class SwitchBranch(bpy.types.Operator):
    """Switch to a branch"""
    bl_idname = "blendgit.switch_branch"
    bl_label = "Switch Branch"

    def execute(self, context: bpy.types.Context):
        if not doc_saved():
            self.report({"ERROR"}, "Need to save first")
            return {"CANCELLED"}
        elif not working_dir_clean():
            self.report(
                {"ERROR"}, "Working directory must be clean (try saving)")
            return {"CANCELLED"}

        if context.window_manager.branches.stash \
                and context.window_manager.branches.stash_message:
            print("Doing stash for",
                  context.window_manager.branches.stash_message)
            stash_save(context.window_manager.branches.stash_message,
                       background=False)
        elif not context.window_manager.branches.stash_message:
            self.report({"ERROR"}, "Please enter a stash message")
            return {"CANCELLED"}

        if len(context.window_manager.branches.branch) == 0:
            return {"CANCELLED"}
        do_git("checkout", context.window_manager.branches.branch)
        bpy.ops.wm.open_mainfile(
            "EXEC_DEFAULT", filepath=bpy.data.filepath)
        self.report({"INFO"}, "Successfully switched branch!")

        return {"FINISHED"}


class CreateBranch(bpy.types.Operator):
    """Create a branch"""
    bl_idname = "blendgit.create_branch"
    bl_label = "Create Branch"

    def execute(self, context: bpy.types.Context):
        new_branch = context.window_manager.branches.new_branch
        do_git("checkout",
               "-b",
               new_branch)
        self.report({"INFO"},
                    f"Created new branch {new_branch}")

        return {"FINISHED"}


def list_branches(self=None, context=None):
    """Returns a list of branches to be passed to SelectBranch"""
    branches_list = []
    if check_repo_exists():
        current_branch = do_git(
            'rev-parse',
            '--abbrev-ref',
            'HEAD').rstrip()
        branches_list.append((current_branch, current_branch, ""))
        for branch in do_git("branch", "--format=%(refname:short)") \
                .split("\n"):
            if not branch:
                break
            elif branch == current_branch:
                continue
            branches_list.append((branch, branch, ""))
    else:
        branches_list = [("", "No repo found", ""), ]

    return branches_list


registry = [
    SwitchBranch,
    CreateBranch,
]
