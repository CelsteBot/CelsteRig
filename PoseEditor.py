import re
import bpy
from . import Classes


class CelsteRig(Classes.CelstePanel):
    bl_idname = 'PANEL1_PT_celste_rig'
    bl_category = 'CelsteRig'
    bl_label = 'Pose Editor'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw_layers(self, master_bone, rig, props, col, context):
        container = col
        row = None
        last = None
        for prop in props[1]:
            if prop['layer'] != master_bone['CELSTE_RIG_ID']:
                layer_name = prop['name']

                new_h_row = False
                if last != None and not last['h_item'] and prop['h_item'] or last != None and last['h_item_end']:
                    new_h_row = True

                if not prop['h_item'] or row == None or new_h_row:
                    row = container.row()

                row.prop(rig, 'layers', index=prop['layer'], toggle=True, text=layer_name)
                last = prop
            else:
                row = None
                last = None
                if not prop['h_item_end']:
                    container = col.box()
                    if prop['name'] != None and prop['name'] != '':
                        container.label(text=prop['name'])
                else:
                    container = col
                    if prop['h_item']:
                        container.separator()

    def sort_layers(self, layers):
        n = len(layers)
    
        for i in range(n):
            for j in range(0, n-i-1):
                current_value = int(re.sub('[^0-9]', '', layers[j][0].split('-')[0]))
                next_value = int(re.sub('[^0-9]', '', layers[j + 1][0].split('-')[0]))
                if current_value > next_value:
                    layers[j], layers[j+1] = layers[j+1], layers[j]

        return layers

    def draw(self, context):
        layout = self.layout

        rig = self.verify_selection(context)
        if rig == None:
            layout.label(text='Select a valid Celste Rig!')
            return

        rig, master_bone = self.verify_selection(context)
        layout.label(text=rig.name)

        layer_column = layout.column()
        # layer_items = []
        for prop in master_bone.items():
            if self.settings['LAYER_TITLE'] in prop[0]:
                self.draw_layers(master_bone, rig, prop, layer_column, context)

        # layer_items = self.sort_layers(layer_items)
        # self.draw_layers(rig, layer_items, layer_column, context)


CLASSES = [CelsteRig]