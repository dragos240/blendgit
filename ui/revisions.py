from typing import Any

from bpy.types import Context, UILayout, UIList

from ..common import get_num_operations, ui_refresh, working_dir_clean
from ..tools.stash import Stash
from ..templates import ToolPanel
from ..tools.revisions import SaveCommit, refresh_revisions, LoadCommit
from ..tools.branches import SwitchToMainBranch


class RevisionList(UIList):
    bl_idname = "BLENDGIT_UL_revision_list"
    bl_label = "Revision List"

    def draw_item(self,
                  context: Context | None,
                  layout: UILayout,
                  data: Any | None,
                  item: Any | None,
                  icon: int | None,
                  active_data: Any,
                  active_property: str | None,
                  index: Any | None = 0,
                  flt_flag: Any | None = 0):
        if item is not None:
            date = item["date"]
            message = item["message"]
            sep = " " * 5
            layout.label(text=f"{date}{sep}{message}")


class RevisionsPanel(ToolPanel):
    """Panel that shows revision history"""
    bl_idname = "BLENDGIT_PT_revision_history"
    bl_label = "Revision History"

    def draw(self, context: Context):
        layout = self.layout
        blendgit = context.window_manager.blendgit
        revision_props = blendgit.revision_properties

        main_row = layout.row()
        main_col = main_row.column()

        if len(revision_props.revision_list) == 0 \
                or blendgit.num_git_operations != get_num_operations():
            blendgit.num_git_operations = get_num_operations()
            revisions = refresh_revisions()
            revision_props.revision_list.clear()
            for entry in revisions:
                revision_entry = revision_props.revision_list.add()
                revision_entry["date"] = entry["date"]
                revision_entry["message"] = entry["message"]
                revision_entry["hash"] = entry["hash"]
            ui_refresh()

        row = main_col.row()
        row.template_list(RevisionList.bl_idname,
                          "",
                          revision_props,
                          "revision_list",
                          revision_props,
                          "revision_list_index")

        row = main_col.row()
        row.operator(LoadCommit.bl_idname, icon="LOOP_BACK")
        row.enabled = working_dir_clean()
        row = main_col.row()
        row.operator(SwitchToMainBranch.bl_idname,
                     icon="FILE_PARENT",
                     text="Switch To Main")
        row.enabled = working_dir_clean()
        if not working_dir_clean():
            row = main_col.row()
            row.label(text="Must stash or commit before switching branch",
                      icon="INFO")
            row = main_col.row()
            col = row.column()
            col.operator(Stash.bl_idname, icon="TRIA_DOWN_BAR")
            col = row.column()
            col.operator(SaveCommit.bl_idname, icon="IMPORT")


registry = [
    RevisionList,
    RevisionsPanel,
]
