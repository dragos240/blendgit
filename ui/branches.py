from ..templates import ToolPanel
from ..tools.branches import SwitchBranch, CreateBranch
from ..tools.register import register_wrap


@register_wrap
class BranchesPanel(ToolPanel):
    """Branch operations"""
    bl_idname = "BLENDGIT_PT_select_branch"
    bl_label = "Branches"

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        row = box.row(align=True)
        row.prop(context.window_manager.branches, "branch", text='')
        row = box.row(align=True)
        row.operator(SwitchBranch.bl_idname)

        box = layout.box()
        row = box.row(align=True)
        row.prop(context.window_manager.branches, "new_branch", text='')
        row = box.row()
        row.operator(CreateBranch.bl_idname)
