import bpy
from . import Classes
from random import randint


class ConvertPanel(Classes.CelstePanel):
    bl_idname = 'PANEL4_PT_convert_rig'
    bl_category = 'CelsteRig'
    bl_label = 'Convert Rig'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        rig = self.verify_selection(context)
        if rig == None:
            obj = context.object
            if obj.type != 'ARMATURE':
                layout.label(text='Select an armature')
                return

            try:
                # check some stuff
                status = obj.pose.bones[0][self.settings['LAYER_TITLE']]
                layer_inspecting = context.scene.layer_inspecting
            except KeyError: # Conversion has not begun
                layout.label(text=f'Convert {context.object.name} to a Celste Rig')
                layout.operator('opr.convert_rig_operator', text='Start Convert')
            except AttributeError: # Blender was closed during the conversion or the conversion was undone
                obj.pose.bones[0].pop(self.settings['LAYER_TITLE'])
                obj.pose.bones[0].pop('PRESETS')
                
CLASSES = [
    ConvertPanel,
]
PROPS = [
]

