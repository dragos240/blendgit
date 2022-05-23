import bpy

from ..templates import ToolPanel
from ..tools.register import register_wrap
from ..tools import lfs
from ..tools.saving import SaveCommit
from ..tools.loading import LoadCommit


@register_wrap
class VersionsPanel(ToolPanel):
    """Versions Operations"""
    bl_idname = "BLENDGIT_PT_versions"
    bl_label = "Versions"

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        lfs.lfs_data_update_async()

        # SAVING
        box = layout.box()
        commit_msg_row = box.row(align=True)
        commit_msg_row.prop(context.window_manager.versions,
                            "commit_message", text='')
        row = box.row(align=True)
        row.prop(context.window_manager.versions, "restore_stash")
        save_commit_button_row = box.row(align=True)
        save_commit_button_row.operator(SaveCommit.bl_idname)

        if not lfs.lfs_installed:
            # Tell user to install git-lfs, disable commit button
            save_commit_button_row.enabled = False
            row = box.row(align=True)
            row.label(text="Please install LFS",
                      icon="INFO")
        elif not lfs.lfs_initialized:
            # Disable commit button, tell user to initialize LFS
            save_commit_button_row.enabled = False
            row = box.row(align=True)
            row.label(text="Enable LFS for your project first!",
                      icon="INFO")
            row = box.row(align=True)
            row.operator(lfs.InitLfs.bl_idname)

        # LOADING
        box = layout.box()
        row = box.row(align=True)
        row.prop(context.window_manager.versions, "commits", text="")
        row = box.row(align=True)
        row.prop(context.window_manager.versions, "stash")
        if context.window_manager.versions.stash:
            row = box.row(align=True)
            row.prop(context.window_manager.versions,
                     "stash_message", text="")
        row = box.row(align=True)
        row.operator(LoadCommit.bl_idname)
