from threading import Thread

import bpy

from ..common import do_git, check_repo_exists


class Stash(bpy.types.Operator):
    bl_idname = "blendgit.stash"
    bl_label = "Stash"

    def execute(self, context: bpy.types.Context):
        return {"FINISHED"}


class StashPop(bpy.types.Operator):
    bl_idname = "blendgit.stash_pop"
    bl_label = "Pop Stash"


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


def stash_pop(background=True):
    def stash():
        do_git("stash", "pop")
    if not background:
        stash()
        return
    thread = Thread(target=stash)
    thread.start()


registry = [
    Stash,
    StashPop,
]
