from bpy.types import Operator, Context

from .files import refresh_files

from ..common import do_git, check_repo_exists, ui_refresh


class Stash(Operator):
    bl_idname = "blendgit.stash"
    bl_label = "Stash"
    bl_description = "Stash all uncommitted changes"

    def stash_save(self):
        def stash():
            if not check_repo_exists():
                return
            do_git("stash", "save", "-u")
            refresh_files()
            ui_refresh()
        stash()
        return

    def execute(self, context: Context):
        self.stash_save()
        self.report({"INFO"}, "Successfully saved stash!")
        return {"FINISHED"}


class StashPop(Operator):
    bl_idname = "blendgit.stash_pop"
    bl_label = "Pop Stash"
    bl_description = "Pop the last stash from the stack"

    def stash_pop(self):
        def stash():
            if not check_repo_exists():
                return
            do_git("stash", "pop")
            refresh_files()
            ui_refresh()
        stash()
        return

    def execute(self, context: Context):
        self.stash_pop()
        self.report({"INFO"}, "Successfully popped stash!")
        return {"FINISHED"}


registry = [
    Stash,
    StashPop,
]
