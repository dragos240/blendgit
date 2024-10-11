from typing import List

from ..common import status


files_list = []
files_list_needs_update = False


def refresh_files() -> List:
    global files_list, files_list_needs_update

    if not files_list or files_list_needs_update:
        files_list = status()
        files_list_needs_update = False

    return files_list


def set_file_list_needs_update():
    global files_list_needs_update
    files_list_needs_update = True
