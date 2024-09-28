import bpy
from bl_ui.space_filebrowser import FileBrowserPanel

from ..templates import ToolPanel


class GitFileList(bpy.types.UIList):
    bl_idname = "BLENDGIT_UL_file_list"

    def draw_item(self, context,
                  layout,
                  data,
                  item,
                  icon,
                  active_data,
                  active_propname):
        pass


class GitFileBrowserPanel(FileBrowserPanel, ToolPanel):
    bl_idname = 'BLENDGIT_PT_file_browser'
    bl_label = 'Files'

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        box = layout.box()
        row = box.row(align=True)
        row.template_list(
            listtype_name=GitFileList.bl_idname,
            list_id="blendgit_file_list",
            dataptr=context.window_manager.blendgit,
        )

        return {'FINISHED'}
