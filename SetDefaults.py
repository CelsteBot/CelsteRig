import bpy
import json
from . import Classes


prev_lay_title = ('previous_layer_title', bpy.props.StringProperty(name='Previous Layer Title', default='LAYER'))

class SetDefaults(Classes.CelstePanel):
    bl_idname = 'PANEL5_PT_set_defaults'
    bl_category = 'CelsteRig'
    bl_label = 'Set Defaults'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        rig = self.verify_selection(context)
        if rig == None:
            layout.label(text='Select a valid Celste Rig!')
            return

        col = layout.column()
        row = col.row()
        row.label(text='Reset Layer Labeling')
        row.prop(context.scene, prev_lay_title[0])
        col.operator('opr.def_layer_label', text='Reset Labels')

class DefLayerOperator(bpy.types.Operator):
    bl_idname = 'opr.def_layer_label'
    bl_label = 'Reset Labels'
    bl_description = 'Reset the Layer names of the active Skeleton to the defaults saved in settings.json'

    def __init__(self) -> None:
        self.settings = json.load(open('C:\\Users\\alexa\\Desktop\\PythonProjects\\RigAddon\\settings.json')) # !!!!!! IMPORTANT !!!!!! CHANGE THIS ON BUILD OR U R DUMB AND STUPID AND IT WONT WORK !!!!!!
        super().__init__()

    def execute(self, context):
        params = (context.scene.previous_layer_title)
        master_bone = None
        for bone in context.object.pose.bones:
            for prop in bone.items():
                if prop[0] == 'CELSTE_RIG_ID':
                    master_bone = bone

        to_delete = []
        for prop in master_bone.items():
            if params in prop[0]:
                print(params[0], 'was in', prop[0])
                to_delete.append(prop[0])

        for i in to_delete:
            master_bone.pop(i)
                
        for layer in self.settings['DEFAULT_LAYER_SETTINGS']:
            layer_name = f"{self.settings['LAYER_TITLE']}_{str(layer['y'])}.{str(layer['x'])}-{str(layer['name'])}"
            master_bone[layer_name] = layer['layer']

        return {'FINISHED'}

CLASSES = [
    SetDefaults,
    DefLayerOperator
]
PROPS = [
    prev_lay_title
]

