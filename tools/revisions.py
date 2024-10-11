from typing import List

from ..common import git_log

revision_list = []
revision_list_needs_update = False


def refresh_revisions() -> List:
    global revision_list, revision_list_needs_update

    if not revision_list or revision_list_needs_update:
        revision_list = git_log()
        revision_list_needs_update = False

    return revision_list


def set_revision_list_need_update():
    global revision_list_needs_update
    revision_list_needs_update = True
