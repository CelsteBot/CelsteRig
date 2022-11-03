import bpy
from . import Classes


class PerfSettings(Classes.CelstePanel):
    bl_idname = 'PANEL2_PT_celste_rig'
    bl_category = 'CelsteRig'
    bl_label = 'Performance Settings'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        verify = self.verify_selection(context)
        layout = self.layout

        if verify == None:
            layout.label(text="Select a valid CelsteRig!")
            return

        arm, master_bone = verify

        props = {}
        for prop in master_bone.items():
            if '_PVAR_' in prop[0]:
                tag = prop[0].split('_')

                if tag[1] not in props.keys():
                    props[tag[1]] = {'name': tag[1]}

                # store the property's path in the props dictionary
                if tag[len(tag) - 1] == 'T':
                    props[tag[1]]['toggle'] = prop[0]
                elif tag[len(tag) - 1] == 'V':
                    props[tag[1]]['value'] = prop[0]
                else:
                    props[tag[1]]['name'] = prop[0]

        for key in props.keys():
            icon = ''
            if master_bone[props[key]['toggle']] == 1:
                icon = 'RESTRICT_VIEW_OFF'
            else:
                icon = 'RESTRICT_VIEW_ON'

            row = layout.row()
            row.label(text=master_bone[props[key]['name']] + ': ')
            if 'value' in props[key].keys():
                row.prop(master_bone, f'["{props[key]["value"]}"]', text='')
            row.operator(f'opr.{key.lower()}_active_operator', icon=icon, text='')




CLASSES = [
    PerfSettings,
]