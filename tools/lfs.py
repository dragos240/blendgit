import bpy

from shutil import which
from os.path import exists, join as path_join, split as path_split

from ..common import get_blendgit, ui_refresh, do_git

def has_lfs() -> bool:
    """Checks if Git LFS is installed"""
    blendgit = get_blendgit()
    if "lfs_installed" in blendgit.git_checks_done:
        return blendgit.git_checks_done["lfs_installed"]
    blendgit.git_checks_done["lfs_installed"] = False
    if which("git-lfs") is not None:
        blendgit.git_checks_done["lfs_installed"] = True
        return True
    return False


def check_lfs_initialized() -> bool:
    """Checks if LFS is initialized"""
    # This will return a list of files tracked by LFS
    # OR it will return an empty string, which can be checked
    # with the 'not' operator
    work_dir = path_split(bpy.data.filepath)[0]
    gitattributes_path = path_join(work_dir, '.gitattributes')
    if not exists(gitattributes_path):
        return False
    with open(gitattributes_path) as f:
        for line in f.readlines():
            if 'lfs' in line:
                return True

    return False


def initialize_lfs(extra_filetypes=()):
    """Initializes LFS with default binary filetypes"""
    if check_lfs_initialized():
        return
    filetypes = {
        # Models
        "*.fbx", "*.obj", "*.max", "*.blend", "*.blender", "*.dae", "*.mb",
        "*.ma", "*.3ds", "*.dfx", "*.c4d", "*.lwo", "*.lwo2", "*.abc",
        "*.3dm", "*.bin", "*.glb",
        # Images
        "*.jpg", "*.jpeg", "*.png", "*.apng", "*.atsc", "*.gif", "*.bmp",
        "*.exr", "*.tga", "*.tiff", "*.tif", "*.iff", "*.pict", "*.dds",
        "*.xcf", "*.leo", "*.kra", "*.kpp", "*.clip", "*.webm", "*.webp",
        "*.svg", "*.svgz", "*.psd",
        # Archives
        "*.zip", "*.7z", "*.gz", "*.rar", "*.tar",
        # Unity
        "*.meta", "*.unity", "*.unitypackage", "*.asset", "*.prefab",
        "*.mat", "*.anim", "*.controller", "*.overrideController",
        "*.physicMaterial", "*.physicsMaterial2D", "*.playable",
        "*.mask", "*.brush", "*.flare", "*.fontsettings", "*.guiskin",
        "*.giparams", "*.renderTexture", "*.spriteatlas", "*.terrainlayer",
        "*.mixer", "*.shadervariants", "*.preset", "*.asmdef",
        # User specified
        *extra_filetypes
    }
    do_git("lfs", "track", *filetypes)

    ui_refresh()


registry = [
]
