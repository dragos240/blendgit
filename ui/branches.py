from ..templates import ToolPanel
from ..tools.branches import SwitchBranch, CreateBranch


class BranchesPanel(ToolPanel):
    """Branch operations"""
    bl_idname = "BLENDGIT_PT_select_branch"
    bl_label = "Branches"

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        row = box.row(align=True)
        row.prop(context.window_manager.blendgit.branches, "branch", text='')
        row = box.row(align=True)
        row.prop(context.window_manager.blendgit.branches, "stash")
        if context.window_manager.blendgit.branches.stash:
            row = box.row(align=True)
            row.prop(context.window_manager.blendgit.branches,
                     "stash_message", text="")
        row = box.row(align=True)
        row.operator(SwitchBranch.bl_idname)

        layout.separator()
        box = layout.box()
        row = box.row(align=True)
        row.prop(context.window_manager.blendgit.branches,
                 "new_branch", text='')
        row = box.row()
        row.operator(CreateBranch.bl_idname)


registry = [
    # BranchesPanel,
]
