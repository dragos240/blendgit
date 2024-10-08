from typing import List

import bpy

from ..common import status


files_list = []
needs_update = False


def refresh_files() -> List:
    global files_list, needs_update
    if not files_list or needs_update:
        files_list = status()
        needs_update = False

    return files_list


def set_needs_update():
    global needs_update
    needs_update = True
