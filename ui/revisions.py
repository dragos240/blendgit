from typing import Any

import bpy
from bpy.types import Context, UILayout, UIList

from ..templates import ToolPanel
from ..tools.revisions import refresh_revisions


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

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        blendgit = context.window_manager.blendgit
        revision_props = blendgit.revision_properties

        box = layout.box()

        if len(revision_props.revision_list) == 0:
            revisions = refresh_revisions()
            for entry in revisions:
                revision_entry = revision_props.revision_list.add()
                revision_entry["date"] = entry["date"]
                revision_entry["message"] = entry["message"]

        box.template_list(RevisionList.bl_idname,
                          "",
                          revision_props,
                          "revision_list",
                          revision_props,
                          "revision_list_index")


registry = [
    RevisionList,
    RevisionsPanel,
]
