#!/usr/bin/env python3
import logging
from os import getenv
import importlib

from bpy.utils import register_class, unregister_class

from . import tools, ui
from .common import log

bl_info = {
    "name": "Blendgit",
    "author": "Nat Osaka",
    "version": (0, 8, 0),
    "blender": (3, 0, 0),
    "description": "Manage versions of a .blend file using Git",
    "warning": "",
    "wiki_url": "",
    "category": "System",
}


modules = [
    tools,
    ui,
]

logging.basicConfig(level=logging.WARN)
if getenv('DEBUG'):
    logging.basicConfig(level=logging.INFO)
logging.getLogger('blender_id').setLevel(logging.DEBUG)
logging.getLogger('blender_cloud').setLevel(logging.DEBUG)


def reload():
    global modules

    for m in modules:
        importlib.reload(m)


_need_reload = "prefs" in locals()
if _need_reload:
    reload()


def register():
    for m in modules:
        if hasattr(m, 'registry'):
            for c in m.registry:
                register_class(c)
        if hasattr(m, 'register'):
            m.register()


def unregister():
    for m in modules:
        if hasattr(m, 'registry'):
            for c in m.registry:
                unregister_class(c)
        if hasattr(m, 'unregister'):
            m.unregister()


if __name__ == '__main__':
    register()
