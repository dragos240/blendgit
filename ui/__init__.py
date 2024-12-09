from bpy.utils import register_class, unregister_class
from bpy.app import handlers

from ..common import ui_refresh_for_handler

from . import files, revisions

modules = [
    files,
    revisions,
]


def register():
    handlers.save_post.append(ui_refresh_for_handler)
    for m in modules:
        if hasattr(m, 'registry'):
            for c in m.registry:
                register_class(c)
        if hasattr(m, 'register'):
            m.register()


def unregister():
    handlers.save_post.remove(ui_refresh_for_handler)
    for m in modules:
        if hasattr(m, 'registry'):
            for c in m.registry:
                unregister_class(c)
        if hasattr(m, 'unregister'):
            m.unregister()
