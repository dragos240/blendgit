import os.path

import bpy

from ..common import do_git, get_repo_name
from ..tools.register import register_wrap


@register_wrap
class SaveCommit(bpy.types.Operator):
    bl_idname = "blendgit.save_commit"
    bl_label = "Save Commit"

    def execute(self, context: bpy.types.Context):
        msg = context.scene.commit_message

        if msg.strip():
            repo_name = get_repo_name()
            if not os.path.isdir(repo_name):
                do_git("init")

            bpy.ops.wm.save_as_mainfile(
                "EXEC_DEFAULT", filepath=bpy.data.filepath)
            add_files(file=os.path.basename(bpy.data.filepath))
            add_files(add_type='category')

            do_git("commit", "-m", msg)
            self.report({"INFO"}, "Success!")
            result = {"FINISHED"}
        else:
            self.report({"ERROR"}, "Comment cannot be empty")
            result = {"CANCELLED"}

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
