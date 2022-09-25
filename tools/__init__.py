from bpy.utils import register_class, unregister_class

from . import lfs, saving, loading, branches, extensions

modules = [
    lfs,
    saving,
    loading,
    branches,
    extensions,
]


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
