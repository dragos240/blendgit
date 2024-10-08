import bpy

from ..templates import ToolPanel


class RevisionsPanel(ToolPanel):
    """Panel that shows revision history"""
    bl_idname = "BLENDGIT_PT_revision_history"
    bl_label = "Revision History"

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        box = layout.box()


registry = [
    RevisionsPanel,
]
