import bpy
from bpy.props import (EnumProperty,
                       BoolProperty,
                       StringProperty,
                       PointerProperty)
from bpy.types import PropertyGroup

from .loading import get_commits
from .branches import list_branches


class VersionProperties(PropertyGroup):
    """Properties for versions section"""
    commit: EnumProperty(
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


class BranchProperties(PropertyGroup):
    """Properties for branches section"""
    stash: BoolProperty(
        name="Stash before load")
    stash_message: StringProperty(
        name="Stash message")
    branch: EnumProperty(
        name="The local branches of the repo",
        items=list_branches)
    new_branch: StringProperty(
        name="The name of the branch to be created")


class BlendgitProperties(PropertyGroup):
    bl_idname = "blendgit.collection"
    bl_label = "BlendgitCollection"

    versions: PointerProperty(type=VersionProperties)
    branches: PointerProperty(type=BranchProperties)


class FileBrowserProperties(PropertyGroup):
    bl_idname = "blendgit.filebrowserproperties"
    bl_label = "FileBrowserProperties"


registry = [
    VersionProperties,
    BranchProperties,
    BlendgitProperties,
    FileBrowserProperties,
]


def register():
    for cls in registry:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass

    bpy.types.WindowManager.blendgit = PointerProperty(type=BlendgitProperties)


def unregister():
    for cls in reversed(registry):
        bpy.utils.unregister_class(cls)

    del bpy.types.WindowManager.blendgit
