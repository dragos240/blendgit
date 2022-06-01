#!/usr/bin/env python3
import logging
from os import getenv

from bpy.utils import register_class, unregister_class

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


# Loaded so that register_wrap will be called for each class
from . import tools, extensions, ui
ui = ui  # Just to make the linter stop complaining
from .common import log
from .tools import register as reg


logging.basicConfig(level=logging.WARN)
if getenv('DEBUG'):
    logging.basicConfig(level=logging.INFO)
logging.getLogger('blender_id').setLevel(logging.DEBUG)
logging.getLogger('blender_cloud').setLevel(logging.DEBUG)


def register():
    reg.order_classes()
    for cls in reg.__bl_classes:
        try:
            register_class(cls)
            log("Registered", cls.__name__)
        except ValueError:
            pass
    extensions.register()


def unregister():
    for cls in reversed(reg.__bl_ordered_classes):
        try:
            unregister_class(cls)
        except ValueError:
            pass
        except RuntimeError:
            pass


if __name__ == '__main__':
    register()
