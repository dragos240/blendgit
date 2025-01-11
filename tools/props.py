from bpy.props import (BoolProperty, CollectionProperty,
                       EnumProperty,
                       IntProperty,
                       StringProperty,
                       PointerProperty)
from bpy.types import PropertyGroup, WindowManager

from .constants import GIT_STATUS_ENUM
from .branches import list_branches


class BranchProperties(PropertyGroup):
    """Properties for branches section"""
    branch: EnumProperty(
        name="The local branches of the repo",
        items=list_branches)
    new_branch: StringProperty(
        name="The name of the branch to be created")


class GitCommit(PropertyGroup):
    """Represents a Git commit

    Attributes:
        date: The date of the commit was made
        message: The commit message
    """
    date: StringProperty(
        name="Date")

    message: StringProperty(
        name="Message")


class RevisionProperties(PropertyGroup):
    """Properties for revisions

    Attributes:
        revision_list: List of revisions
        revision_list_index: Selected index in the list
    """
    revision_list: CollectionProperty(
        name="Revision List",
        type=GitCommit)

    revision_list_index: IntProperty()

    pending_commit_message: StringProperty(
        name="Pending Commit")


class GitFile(PropertyGroup):
    """Represents a file in the repository

    Attributes:
        name: Name of the file
        path: Path to the file
        status: Commit status
    """
    name: StringProperty(
        name="File Name")

    path: StringProperty(
        name="Path")

    status: EnumProperty(
        name="Commit Status",
        items=GIT_STATUS_ENUM)  # type: ignore


class FileBrowserProperties(PropertyGroup):
    files_list: CollectionProperty(
        type=GitFile)

    files_list_index: IntProperty(
        name="File List")


class BlendgitProperties(PropertyGroup):
    bl_idname = "blendgit.collection"
    bl_label = "BlendgitCollection"

    branch_properties: PointerProperty(type=BranchProperties)
    file_properties: PointerProperty(type=FileBrowserProperties)
    revision_properties: PointerProperty(type=RevisionProperties)
    num_revision_list_refreshes: IntProperty()
    num_file_list_refreshes: IntProperty()
    working_dir_is_clean: BoolProperty()
    current_branch: StringProperty()
    git_checks_done: PointerProperty(type=PropertyGroup)


registry = [
    BranchProperties,
    GitFile,
    FileBrowserProperties,
    GitCommit,
    RevisionProperties,
    BlendgitProperties,
]


def post_register():
    WindowManager.blendgit = PointerProperty(type=BlendgitProperties)


def pre_unregister():
    try:
        getattr(WindowManager, "blendgit")
        del WindowManager.blendgit
    except AttributeError:
        pass
