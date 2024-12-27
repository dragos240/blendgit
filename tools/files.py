from typing import List

from ..common import status


files_list = []


def refresh_files() -> List:
    global files_list

    files_list = status()

    return files_list
