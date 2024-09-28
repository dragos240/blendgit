import bpy

from ..templates import ToolPanel


class RevisionsPanel(ToolPanel):
    """Panel that shows revision history"""
    bl_idname = "BLENDGIT_PT_revision_history"
    bl_label = "Revision History"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        pass

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        box = layout.box()
        row = box.row(align=True)
        return {'FINISHED'}


registry = [
    RevisionsPanel,
]
