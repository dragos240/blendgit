from typing import Any
import bpy
from bpy.types import Context, UILayout

from ..templates import ToolPanel
from ..tools import files as toolsfiles
from ..tools.loading import LoadCommit, StashPop
from ..tools.saving import SaveCommit, Stash


class GitFileList(bpy.types.UIList):
    bl_idname = "BLENDGIT_UL_file_list"

    def draw_item(self,
                  context: Context | None,
                  layout: UILayout,
                  data: Any | None,
                  item: Any | None,
                  icon: int | None,
                  active_data: Any,
                  active_property: str | None,
                  index: Any | None = 0,
                  flt_flag: Any | None = 0
                  ):
        if item is not None:
            layout.label(text=item["name"], icon="FILE")


class GitFileBrowserPanel(ToolPanel):
    bl_idname = 'BLENDGIT_PT_file_browser'
    bl_label = 'Files'

    def draw(self, context):
        layout = self.layout
        blendgit = context.window_manager.blendgit
        file_props = blendgit.file_properties
        main_col = layout.column()
        main_row = main_col.row()
        split = main_row.split(factor=0.6)
        header_sep = " " * 9
        filepath_row = split.row()
        filepath_row.label(text=header_sep + "Filepath")
        status_row = split.row()
        status_row.label(text="Status")
        status_row.alignment = "RIGHT"

        if len(file_props.files_list) == 0:
            files = toolsfiles.refresh_files()
            for entry in files:
                file_entry = file_props.files_list.add()
                file_entry["name"] = entry["file_path"]

        # Add the GitFileList to the panel
        row = main_col.row()
        row.template_list(GitFileList.bl_idname,
                          "",
                          file_props,
                          "files_list",
                          file_props,
                          "files_list_index")

        col = row.column()

        col.separator()
        col.operator(SaveCommit.bl_idname, icon="IMPORT", text="")

        col.separator()
        col.operator(LoadCommit.bl_idname, icon="LOOP_BACK", text="")
        col.operator(Stash.bl_idname, icon="TRIA_DOWN_BAR", text="")
        col.operator(StashPop.bl_idname, icon="TRIA_UP_BAR", text="")


registry = [
    GitFileList,
    GitFileBrowserPanel,
]
