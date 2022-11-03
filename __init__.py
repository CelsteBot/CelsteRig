import bpy
from . import SetDefaults, PoseEditor, RigConvert, RigEdit, PerfSettings


bl_info = {
    "name": "Celste Rig",
    "category": "Rigging",
    "author": "Celste Bot",
    "blender": (3, 3, 0),
    "description":"Generate Celste rigs for posing and animating humanoid characters.",
    "version":(0, 2, 1)
}    

CLASSES = [
    *PoseEditor.CLASSES,
    *PerfSettings.CLASSES,
    *RigEdit.CLASSES,
    *RigConvert.CLASSES,
    *SetDefaults.CLASSES,
]
PROPS = [
    *SetDefaults.PROPS,
    *RigConvert.PROPS
]

def register():
    print('registered', bl_info['name'])
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

    for klass in CLASSES:
        print(klass.bl_idname)
        bpy.utils.register_class(klass)

def unregister():
    print('unregistered', bl_info['name'])
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)

if __name__ == '__main__':
    register()

