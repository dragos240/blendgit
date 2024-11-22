from bpy.utils import register_class, unregister_class

from . import lfs, branches, props, revisions, stash

modules = [
    lfs,
    branches,
    props,
    revisions,
    stash,
]


def register():
    for m in modules:
        if hasattr(m, 'registry'):
            for c in m.registry:
                try:
                    register_class(c)
                except ValueError:
                    pass
        if hasattr(m, 'register'):
            m.register()
        if hasattr(m, "post_register"):
            m.post_register()


def unregister():
    for m in modules:
        if hasattr(m, "pre_unregister"):
            m.pre_unregister()
        if hasattr(m, 'registry'):
            for c in m.registry:
                unregister_class(c)
        if hasattr(m, 'unregister'):
            m.unregister()
