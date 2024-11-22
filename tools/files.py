from typing import List

from ..common import status


refresh_files_list = False
files_list = []


def set_refresh():
    global refresh_files_list
    refresh_files_list = True


def get_files() -> List:
    return files_list


def refresh_files() -> List:
    global files_list

    files_list = status()

    return files_list
