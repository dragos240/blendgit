import os.path
from threading import Thread

import bpy
from bpy.props import StringProperty

from ..common import do_git, check_repo_exists, get_work_dir
from .lfs import initialize_lfs
from .loading import refresh_commit_list_async


class SaveCommit(bpy.types.Operator):
    """Save and commit latest changes"""
    bl_idname = "blendgit.save_commit"
    bl_label = "Save Commit"

    def execute(self, context: bpy.types.Context):
        msg = context.window_manager.versions.commit_message

        if msg.strip():
            if not check_repo_exists():
                do_git("init")
                do_git("config", "--local", "core.autocrlf", "false")
                initialize_lfs()
                create_gitignore()

            if context.window_manager.versions.restore_stash:
                stash_pop(background=False)
                print("Popped stash")

            bpy.ops.wm.save_as_mainfile(
                "EXEC_DEFAULT", filepath=bpy.data.filepath)
            add_files(file=os.path.basename(bpy.data.filepath))
            add_files(add_type='category')

            do_git("commit", "-am", msg)
            self.report({"INFO"}, "Success!")
            refresh_commit_list_async()
            result = {"FINISHED"}
        else:
            self.report({"ERROR"}, "Comment cannot be empty")
            result = {"CANCELLED"}

        msg = StringProperty(
            name="Comment",
            description="Commit message")

        return result


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
            for item in getattr(bpy.data, category):
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
    gitignore = (
        "*.blend*",
        "!*.blend",
        "*.fbx",
        "*.glb",
        "*.gltf",
    )
    work_dir = get_work_dir()
    gitignore_path = os.path.join(work_dir, '.gitignore')
    with open(gitignore_path, 'w', newline='\n') as f:
        f.write("\n".join(gitignore))
    do_git("add", '.gitignore')


def stash_pop(background=True):
    def stash():
        do_git("stash", "pop")
    if not background:
        stash()
        return
    thread = Thread(target=stash)
    thread.start()


registry = [
    SaveCommit,
]
