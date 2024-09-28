from bpy.utils import register_class, unregister_class

from . import lfs, saving, loading, branches, props

modules = [
    lfs,
    saving,
    loading,
    branches,
    props,
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


def unregister():
    for m in modules:
        if hasattr(m, 'registry'):
            for c in m.registry:
                unregister_class(c)
        if hasattr(m, 'unregister'):
            m.unregister()
