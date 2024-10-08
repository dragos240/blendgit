from collections import OrderedDict


GIT_STATUS = OrderedDict([
    (
        "untracked",
        (
            "UNTRACKED",
            "File exists in the working directory but is not yet being tracked by Git",
        ),
    ),
    (
        "unmodified",
        (
            "UNMODIFIED",
            "File is being tracked by Git, and there are no changes to it since the last commit",
        ),
    ),
    (
        "modified",
        (
            "MODIFIED",
            "File has been changed in the working directory but has not yet been staged",
        ),
    ),
    (
        "staged",
        (
            "STAGED",
            "File is staged after using git add, meaning it's in the staging area and ready to be included in the next commit",
        ),
    ),
    (
        "committed",
        (
            "COMMITTED",
            "File's changes have been saved to the repository's history",
        ),
    ),
    (
        "deleted",
        (
            "DELETED",
            "File has been deleted from the working directory and is tracked by Git",
        ),
    ),
    (
        "renamed",
        (
            "RENAMED",
            "File has been renamed or moved within the working directory",
        ),
    ),
    (
        "ignored",
        (
            "IGNORED",
            "File is listed in the .gitignore file and is not tracked by Git",
        ),
    ),
])


GIT_STATUS_ENUM = [
    (status, status.title(), GIT_STATUS[status][1], GIT_STATUS[status][0], i)
    for i, status in enumerate(GIT_STATUS.keys())
]
