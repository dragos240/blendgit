from typing import Any, Dict
from bpy.types import Context, UILayout, UIList

from ..templates import ToolPanel
from ..common import get_num_operations
from ..tools.files import refresh_files
from ..tools.revisions import SaveCommit, StageAll, StageFile
from ..tools.stash import Stash, StashPop


class GitFileList(UIList):
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
            # Draw a file entry line
            main_row = layout.row()
            split = main_row.split(factor=0.35)
            filepath_ui = split.row()
            status_ui = split.row(align=True)
            status_ui.alignment = "LEFT"
            split = split.split()
            staged_ui = split.row(align=True)
            staged_ui.alignment = "CENTER"

            filepath_ui.label(text=item["name"])
            status_ui.label(text=item["status"])
            staged_ui.label(text="",
                            icon=("CHECKMARK" if item["staged"] else "NONE"))


class GitFileBrowserPanel(ToolPanel):
    bl_idname = 'BLENDGIT_PT_file_browser'
    bl_label = 'Files'

    def draw_files(self,
                   context: Context):
        blendgit = context.window_manager.blendgit
        file_props = blendgit.file_properties
        files = refresh_files()
        file_props.files_list.clear()
        for entry in files:
            file_entry = file_props.files_list.add()
            file_entry["name"] = entry["file_path"]
            file_entry["status"] = entry["status"]
            file_entry["staged"] = entry["staged"]

    def draw(self, context: Context):
        layout = self.layout

        blendgit = context.window_manager.blendgit
        file_props = blendgit.file_properties

        main_col = layout.column()

        header_row = main_col.row()
        split = header_row.split()
        filepath_row = split.row()
        filepath_row.label(text="Filepath")
        split = header_row.split()
        status_row = split.row()
        status_row.label(text="Status")
        staged_row = split.row()
        staged_row.label(text="Staged")

        if len(file_props.files_list) == 0 \
                or blendgit.num_git_operations != get_num_operations():
            print(1, blendgit.num_git_operations)  # FIXME
            blendgit.num_git_operations = get_num_operations()
            print(2, blendgit.num_git_operations)  # FIXME
            self.draw_files(context)

        # Add the GitFileList to the panel
        list_row = main_col.row()
        list_row.template_list(GitFileList.bl_idname,
                               "",
                               file_props,
                               "files_list",
                               file_props,
                               "files_list_index")

        col = list_row.column()

        col.separator()
        col.operator(StageFile.bl_idname, icon="ADD", text="")
        col.operator(StageAll.bl_idname, icon="COLLECTION_NEW", text="")

        col.separator()
        col.operator(Stash.bl_idname, icon="TRIA_DOWN_BAR", text="")
        col.operator(StashPop.bl_idname, icon="TRIA_UP_BAR", text="")

        list_row = main_col.row()
        list_row.operator(SaveCommit.bl_idname, icon="IMPORT")
        list_row.separator_spacer()
        list_row.separator_spacer()


registry = [
    GitFileList,
    GitFileBrowserPanel,
]
