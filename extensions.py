import bpy
from bpy.props import (EnumProperty,
                       BoolProperty,
                       StringProperty,
                       PointerProperty)
from bpy.types import PropertyGroup

from .tools.register import register_wrap
from .tools.loading import get_commits
from .tools.branches import list_branches


@register_wrap
class VersionProperties(PropertyGroup):
    """Properties for versions section"""
    commits: EnumProperty(
        name="Which previously-saved commit to restore",
        items=get_commits)
    commit_message: StringProperty(
        name="Commit message")
    stash: BoolProperty(
        name="Stash before load")
    stash_message: StringProperty(
        name="Stash message")
    restore_stash: BoolProperty(
        name="Also restore stash")


@register_wrap
class BranchProperties(PropertyGroup):
    """Properties for branches section"""
    branch: bpy.props.EnumProperty(
        name="The local branches of the repo",
        items=list_branches)
    new_branch: StringProperty(
        name="The name of the branch to be created")


def register():
    bpy.types.WindowManager.versions = PointerProperty(type=VersionProperties)
    bpy.types.WindowManager.branches = PointerProperty(type=BranchProperties)
