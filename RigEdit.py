import bpy
from . import Classes
from random import randint


class RigEditPanel(Classes.CelstePanel):
    bl_idname = 'PANEL3_PT_celste_rig'
    bl_category = 'CelsteRig'
    bl_label = 'Rig Editor'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        arm = self.verify_selection(context)
        layout = self.layout
        if arm == None:
            if 'CELSTE_RIG_OBJ_ID' not in context.object.keys():
                layout.label(text='Select a valid Celste Rig!')
                return
            
        arm, master_bone = arm

        check_keys = []
        for item in master_bone.items():
            check_keys.append(item[0])

        # Layer Data Display
        if 'PRESETS' in check_keys:
                # check if needed information exists
                layer_inspecting = 0
                try:
                    layer_inspecting = context.scene.layer_inspecting
                except:
                    arm[1].pop('PRESETS')
                    return

                col = layout.column()
                box = False
                layer_data = arm[1]['LAYER_DATA'][layer_inspecting]

                if layer_data['layer'] != arm[1]['CELSTE_RIG_ID']:
                    # editing layer display
                    row = col.row()
                    row.prop(context.scene, 'layer_name', text='Layer Name')

                    row = col.row()
                    row.prop(context.scene, 'layer_layer', text='Layer Index')

                    row = col.row()
                    row.prop(context.scene, 'h_item', toggle=1, text='Horrizontal Item')
                    if layer_data['h_item']:
                        row.prop(context.scene, 'h_item_end', toggle=1, text='End Horrizontal')

                    row = col.row()
                    row.operator('opr.layer_up_operator')
                    row.operator('opr.layer_down_operator')
                else:
                    box = True
                    row = col.row()
                    # editing box display
                    if layer_data['h_item_end']:
                        row.label(text='End ' + layer_data['name'] + ' Box')
                        row = col.row()
                        row.prop(context.scene, 'h_item', toggle=1, text='Add Space After Box')
                    else:
                        row.label(text='Box Start')
                        row = col.row()
                        row.prop(context.scene, 'layer_name', text='Layer Name')

                    row = col.row()
                    row.operator('opr.layer_up_operator', text='Move Box Up')
                    row.operator('opr.layer_down_operator', text='Move Box Down')

                row = col.row()
                row.operator('opr.last_layer_opeator')
                row.label(text=str(layer_inspecting))
                row.operator('opr.next_layer_opeator')

                row = col.row()
                row.prop(context.scene, 'convert_presets', text='Change Rig Preset')

                if not box:
                    row = col.row()
                    row.operator('opr.box_add_operator')

                row = col.row()
                if box:
                    row.operator('opr.box_delete_operator')
                else:
                    row.operator('opr.layer_delete_operator')
                row.operator('opr.layer_add_operator')

                row = col.row()
                row.operator('opr.convert_finish_operator')
                return

        # Perfoirmance Variables Display
        if 'PERF_CONFIG' in check_keys:
            for key in check_keys:
                if '_PVAR_N' in key:
                    layout.prop(master_bone, f'["{key}"]', text=key.split('_')[1] + ' Modifier Name: ')   

            layout.separator()

            layout.label(text="Select objects to change modifier settings")
            layout.operator('opr.perf_var_edit_finish_operator')

            return

        layout.label(text='omg were changing rigs!?!?!?')
        layout.operator('opr.convert_rig_operator')
        layout.operator('opr.perf_var_config_operator')


# Layer Data Classes
class LastLayerOperator     (Classes.CelsteOperator):
    bl_idname = 'opr.last_layer_opeator'
    bl_label = '<'
    bl_description = 'Last layer'

    def execute(self, context):
        last = context.scene.layer_inspecting
        master_bone = self.verify_selection(context)[1]
        context.scene.layer_inspecting -= 1

        if context.scene.layer_inspecting < 0:
            context.scene.layer_inspecting = len(master_bone[self.settings['LAYER_TITLE']]) - 1

        current = context.scene.layer_inspecting

        master_bone[self.settings['LAYER_TITLE']][last]['name'] =   context.scene.layer_name
        master_bone[self.settings['LAYER_TITLE']][last]['h_item'] = context.scene.h_item
        master_bone[self.settings['LAYER_TITLE']][last]['h_item_end'] = context.scene.h_item_end
        master_bone[self.settings['LAYER_TITLE']][last]['layer'] =  context.scene.layer_layer

        context.scene.layer_name =  master_bone[self.settings['LAYER_TITLE']][current]['name'] 
        context.scene.h_item =      master_bone[self.settings['LAYER_TITLE']][current]['h_item']
        context.scene.h_item_end =  master_bone[self.settings['LAYER_TITLE']][current]['h_item_end']
        context.scene.layer_layer = master_bone[self.settings['LAYER_TITLE']][current]['layer']

        return {'FINISHED'}
class NextLayerOperator     (Classes.CelsteOperator):
    bl_idname = 'opr.next_layer_opeator'
    bl_label = '>'
    bl_description = 'Next layer'

    def execute(self, context):
        last = context.scene.layer_inspecting
        master_bone = self.verify_selection(context)[1]
        context.scene.layer_inspecting += 1

        if last >= len(master_bone[self.settings['LAYER_TITLE']]) - 1:
            context.scene.layer_inspecting = 0

        current = context.scene.layer_inspecting

        master_bone[self.settings['LAYER_TITLE']][last]['name'] =   context.scene.layer_name
        master_bone[self.settings['LAYER_TITLE']][last]['h_item'] = context.scene.h_item
        master_bone[self.settings['LAYER_TITLE']][last]['h_item_end'] = context.scene.h_item_end
        master_bone[self.settings['LAYER_TITLE']][last]['layer'] =  context.scene.layer_layer

        context.scene.layer_name =  master_bone[self.settings['LAYER_TITLE']][current]['name'] 
        context.scene.h_item =      master_bone[self.settings['LAYER_TITLE']][current]['h_item']
        context.scene.h_item_end =  master_bone[self.settings['LAYER_TITLE']][current]['h_item_end']
        context.scene.layer_layer = master_bone[self.settings['LAYER_TITLE']][current]['layer']

        return {'FINISHED'}

class LayerUpOperator       (Classes.CelsteOperator):
    bl_idname = 'opr.layer_up_operator'
    bl_label = 'Move Layer Up'
    bl_description = 'Moves layer display up in list'

    def execute(self, context):
        master_bone = self.verify_selection(context)[1]
        data_name = self.settings['LAYER_TITLE']

        last = context.scene.layer_inspecting
        context.scene.layer_inspecting -= 1

        if context.scene.layer_inspecting < 0:
            context.scene.layer_inspecting = len(master_bone[data_name]) - 1

        current = context.scene.layer_inspecting
        items = master_bone[data_name]
        data = items[last]
        items.pop(last)
        items.insert(current, data)
        master_bone[data_name] = items

        context.scene.layer_name =  master_bone[data_name][current]['name'] 
        context.scene.h_item =      master_bone[data_name][current]['h_item']
        context.scene.h_item_end =  master_bone[data_name][current]['h_item_end']
        context.scene.layer_layer = master_bone[data_name][current]['layer']

        return {'FINISHED'}
class LayerDownOperator     (Classes.CelsteOperator):
    bl_idname = 'opr.layer_down_operator'
    bl_label = 'Move Layer Down'
    bl_description = 'Moves layer display down in list'

    def execute(self, context):
        master_bone = self.verify_selection(context)[1]
        data_name = self.settings['LAYER_TITLE']

        last = context.scene.layer_inspecting
        context.scene.layer_inspecting += 1

        if last >= len(master_bone[self.settings['LAYER_TITLE']]) - 1:
            context.scene.layer_inspecting = 0

        current = context.scene.layer_inspecting
        items = master_bone[data_name]
        data = items[last]
        items.pop(last)
        items.insert(current, data)
        master_bone[data_name] = items

        context.scene.layer_name =  master_bone[self.settings['LAYER_TITLE']][current]['name'] 
        context.scene.h_item =      master_bone[self.settings['LAYER_TITLE']][current]['h_item']
        context.scene.h_item_end =  master_bone[self.settings['LAYER_TITLE']][current]['h_item_end']
        context.scene.layer_layer = master_bone[self.settings['LAYER_TITLE']][current]['layer']

        return {'FINISHED'}

class LayerDeleteOperator   (Classes.CelsteOperator):
    bl_idname = 'opr.layer_delete_operator'
    bl_label = 'Delete Layer Display'
    bl_description = "Hides this layer in the Celste Pose view (Doesn't remove any data from your armature)"

    def execute(self, context):
        master_bone = self.verify_selection(context)[1]
        tmp_list = master_bone[self.settings['LAYER_TITLE']]
        tmp_list.pop(context.scene.layer_inspecting)
        master_bone[self.settings['LAYER_TITLE']] = tmp_list

        context.scene.layer_inspecting += 1

        if context.scene.layer_inspecting >= len(master_bone[self.settings['LAYER_TITLE']]):
            context.scene.layer_inspecting = 0

        current = context.scene.layer_inspecting

        context.scene.layer_name =  master_bone[self.settings['LAYER_TITLE']][current]['name'] 
        context.scene.h_item =      master_bone[self.settings['LAYER_TITLE']][current]['h_item']
        context.scene.h_item_end =  master_bone[self.settings['LAYER_TITLE']][current]['h_item_end']
        context.scene.layer_layer = master_bone[self.settings['LAYER_TITLE']][current]['layer']

        return {'FINISHED'}
class LayerAddOperator      (Classes.CelsteOperator):
    bl_idname = 'opr.layer_add_operator'
    bl_label = 'Add Layer Display'
    bl_description = "Add a layer display to the Celste Pose view"

    def execute(self, context):
        master_bone = self.verify_selection(context)[1]
        index = context.scene.layer_inspecting
        tmp_list = master_bone[self.settings['LAYER_TITLE']]
        tmp_list.insert(index + 1, {'name': 'Layer ' + str(len(tmp_list) + 1), 'h_item': False, 'h_item_end': False,'layer': 0})
        master_bone[self.settings['LAYER_TITLE']] = tmp_list
        
        context.scene.layer_inspecting += 1

        if context.scene.layer_inspecting >= len(master_bone[self.settings['LAYER_TITLE']]):
            context.scene.layer_inspecting = 0

        current = context.scene.layer_inspecting

        context.scene.layer_name =  master_bone[self.settings['LAYER_TITLE']][current]['name'] 
        context.scene.h_item =      master_bone[self.settings['LAYER_TITLE']][current]['h_item']
        context.scene.h_item_end =  master_bone[self.settings['LAYER_TITLE']][current]['h_item_end']
        context.scene.layer_layer = master_bone[self.settings['LAYER_TITLE']][current]['layer']

        return{'FINISHED'}

class BoxDeleteOperator     (Classes.CelsteOperator):
    bl_idname = 'opr.box_delete_operator'
    bl_label = 'Delete Box'
    bl_description = "Remove this box from the display"

    def execute(self, context):
        master_bone = self.verify_selection(context)[1]
        index = context.scene.layer_inspecting

        tmp_list = master_bone[self.settings['LAYER_TITLE']]
        popped = tmp_list.pop(context.scene.layer_inspecting)

        celste_id = master_bone['CELSTE_RIG_ID']
        found = False
        if popped['h_item_end']:
            while not found:
                index += 1
                if tmp_list[index]['layer'] == celste_id:
                    found = True
        else:
            while not found:
                index -= 1
                if tmp_list[index]['layer'] == celste_id:
                    tmp_list.pop(index)
                    found = True

        master_bone[self.settings['LAYER_TITLE']] = tmp_list

        if context.scene.layer_inspecting >= len(master_bone[self.settings['LAYER_TITLE']]):
            context.scene.layer_inspecting = 0

        current = context.scene.layer_inspecting

        context.scene.layer_name =  master_bone[self.settings['LAYER_TITLE']][current]['name'] 
        context.scene.h_item =      master_bone[self.settings['LAYER_TITLE']][current]['h_item']
        context.scene.h_item_end =  master_bone[self.settings['LAYER_TITLE']][current]['h_item_end']
        context.scene.layer_layer = master_bone[self.settings['LAYER_TITLE']][current]['layer']

        return { 'FINISHED' }
class BoxAddOperator        (Classes.CelsteOperator):
    bl_idname = 'opr.box_add_operator'
    bl_label = 'Add Layer Box'
    bl_description = "Add a box to group the layers"

    def execute(self, context):
        master_bone = self.verify_selection(context)[1]
        index = context.scene.layer_inspecting
        celste_id = master_bone['CELSTE_RIG_ID']

        tmp_list = master_bone[self.settings['LAYER_TITLE']]
        tmp_list.insert(index, {'name': '', 'h_item': False, 'h_item_end': False,'layer': celste_id})
        tmp_list.insert(index + 2, {'name': '', 'h_item': False, 'h_item_end': True,'layer': celste_id})
        

        master_bone[self.settings['LAYER_TITLE']] = tmp_list
        
        context.scene.layer_name =  master_bone[self.settings['LAYER_TITLE']][index]['name'] 
        context.scene.h_item =      master_bone[self.settings['LAYER_TITLE']][index]['h_item']
        context.scene.h_item_end =  master_bone[self.settings['LAYER_TITLE']][index]['h_item_end']
        context.scene.layer_layer = master_bone[self.settings['LAYER_TITLE']][index]['layer']

        return{'FINISHED'}

class StartRigEditOperator  (Classes.CelsteOperator):
    bl_idname = 'opr.convert_rig_operator'
    bl_label = 'Edit Layer Display'
    bl_description = 'Convert active rig into a Celste Rig'

    def enum_items(self, context):
        out = []
        for layer_settings in self.settings['DEFAULT_LAYER_SETTINGS'].keys():
            out.append((layer_settings.upper(), layer_settings, 'Automatically convert display data to be configured for ' + layer_settings))

        return out

    # Start the rig conversion process including creating all the data that will be needed for the process
    def execute(self, context):
        master_bone = self.verify_selection(context)

        def enum_change(self, context):
            convert_data = []
            obj = context.object
            master_bone = obj.pose.bones[0]
            pull_data = master_bone['PRESETS']['pull_data']

            # create data needed for converting
            x = 0
            reorder = False
            for i in range(len(obj.data.layers)):
                # check if layer has any bones
                bone_check = False
                for bone in obj.data.bones:
                    if bone.layers[i]:
                        bone_check = True
                        break

                if not bone_check:
                    continue

                # set layer display data
                default_layers = master_bone['PRESETS'][str(context.scene.convert_presets)]
                data_template = {'name': 'Layer ' + str(x), 'h_item': False, 'h_item_end': False, 'layer': i}
                
                for layer_data in default_layers:
                    if layer_data['layer'] == i:
                        reorder = True
                        data_template = {'name': layer_data['name'], 'h_item': layer_data['h_item'], 'h_item_end': layer_data['h_item_end'], 'layer': layer_data['layer']}

                convert_data.append(data_template)
                x += 1

            out_list = []
            in_list = convert_data
            if reorder:
                for layer_preset in default_layers:
                    for i, layer in enumerate(in_list):
                        if layer['name'] == layer_preset['name']:
                            out_list.append(layer)
                            in_list.pop(i)
                            break
            for layer in in_list:
                out_list.append(layer)

            master_bone[pull_data] = out_list

            try:
                # Correct the display after converting
                current = context.scene.layer_inspecting
                context.scene.layer_name =  master_bone[pull_data][current]['name'] 
                context.scene.h_item =      master_bone[pull_data][current]['h_item']
                context.scene.h_item_end =  master_bone[pull_data][current]['h_item_end']
                context.scene.layer_layer = master_bone[pull_data][current]['layer']
            except AttributeError:
                print('Convert Started')

        if master_bone == None:
            master_bone = context.object.pose.bones[0]
            
            setattr(bpy.types.Scene, 'convert_presets', bpy.props.EnumProperty(items=self.enum_items(context), name='Convert Presets', description="Automatically configure rig for common rig types(Will overwrite any layer display data you've set)", default='RIGIFY', update=enum_change))
            master_bone['PRESETS'] = self.settings['DEFAULT_LAYER_SETTINGS']
            master_bone['PRESETS']['pull_data'] = self.settings['LAYER_TITLE']
            master_bone['CELSTE_RIG_ID'] = randint(100000, 999999) # I'm scaming so hard. You bitches really thought the ID ment something lol
            enum_change(self, context)

            # create scene properties
            convert_data = master_bone[self.settings['LAYER_TITLE']]
            setattr(bpy.types.Scene, 'layer_name'      , bpy.props.StringProperty  (name='Layer Name',           description='Name of active layer',                      default=convert_data[0]['name']   ))
            setattr(bpy.types.Scene, 'layer_layer'     , bpy.props.IntProperty     (name='Layer Layer',          description='Index of the layer (0-31)',                 default=convert_data[0]['layer'], min=0, max=31))
            setattr(bpy.types.Scene, 'layer_inspecting', bpy.props.IntProperty     (name='Layer Inspecting',     description='Index of the active layer (0-31)',          default=0                         ))
            setattr(bpy.types.Scene, 'h_item'          , bpy.props.BoolProperty    (name='Horizontal Group',     description='Put this layer into a horizontal group(grouped with adjacent horizontal items in the layer list)', default=convert_data[0]['h_item']))
            setattr(bpy.types.Scene, 'h_item_end'      , bpy.props.BoolProperty    (name='Horizontal Group End', description='End this horrizontal group(used when 2 horrizontal groups are adjacent)', default=convert_data[0]['h_item_end']))

        else:
            master_bone = master_bone[1]

            try:
                # Cancel the conversion
                master_bone.pop('PRESETS')
                master_bone.pop(self.settings['LAYER_NAME'])

                delattr(bpy.types.Scene, 'layer_name')
                delattr(bpy.types.Scene, 'h_item')
                delattr(bpy.types.Scene, 'h_item_end')
                delattr(bpy.types.Scene, 'layer_layer')
                delattr(bpy.types.Scene, 'layer_inspecting')
                delattr(bpy.types.Scene, 'convert_presets')
            except:
                # edit
                master_bone['PRESETS'] = self.settings['DEFAULT_LAYER_SETTINGS']
                master_bone['PRESETS']['pull_data'] = self.settings['LAYER_TITLE']
                convert_data = master_bone[self.settings['LAYER_TITLE']]
                setattr(bpy.types.Scene, 'layer_name'      , bpy.props.StringProperty  (name='Layer Name',           description='Name of active layer',                      default=convert_data[0]['name']   ))
                setattr(bpy.types.Scene, 'layer_layer'     , bpy.props.IntProperty     (name='Layer Layer',          description='Index of the layer (0-31)',                 default=convert_data[0]['layer']  ))
                setattr(bpy.types.Scene, 'layer_inspecting', bpy.props.IntProperty     (name='Layer Inspecting',     description='Index of the active layer (0-31)',          default=0                         ))
                setattr(bpy.types.Scene, 'h_item'          , bpy.props.BoolProperty    (name='Horizontal Group',     description='Put this layer into a horizontal group(grouped with adjacent horizontal items in the layer list)', default=convert_data[0]['h_item']))
                setattr(bpy.types.Scene, 'h_item_end'      , bpy.props.BoolProperty    (name='Horizontal Group End', description='End this horrizontal group(used when 2 horrizontal groups are adjacent)', default=convert_data[0]['h_item_end']))
                setattr(bpy.types.Scene, 'convert_presets' , bpy.props.EnumProperty    (items=self.enum_items(context), name='Convert Presets', description="Automatically configure rig for common rig types(Will overwrite any layer display data you've set)", default='RIGIFY', update=enum_change))

        return {'FINISHED'}
class FinishRigEditOperator (Classes.CelsteOperator):
    bl_idname = 'opr.convert_finish_operator'
    bl_label = 'Finish'
    bl_description = 'Finish conversion'

    def execute(self, context):
        master_bone = self.verify_selection(context)[1]
        master_bone.pop('PRESETS')

        delattr(bpy.types.Scene, 'layer_name')
        delattr(bpy.types.Scene, 'h_item')
        delattr(bpy.types.Scene, 'h_item_end')
        delattr(bpy.types.Scene, 'layer_layer')
        delattr(bpy.types.Scene, 'layer_inspecting')
        delattr(bpy.types.Scene, 'convert_presets')
        return {'FINISHED'}

# Performance Variables Classes
class PerfVarConfig         (Classes.CelsteOperator):
    bl_idname = 'opr.perf_var_config_operator'
    bl_label = 'Configure Performance Settings'
    bl_description = 'Detect items within child objects that can be configured for better viewport performance.'

    def execute(self, context):
        # create the perf_var contianer
        verify = self.verify_selection(context)
        if verify == None:
            return { 'CANCELLED' }

        # vars
        arm, master_bone = verify
        obj = context.object
        data = {}

        # find all modifiers in children
        for child in obj.children_recursive:
            for m in child.modifiers:
                # check if they're performance modifiers
                m_type = m.type
                if m_type not in self.settings['PERF_MODIFIERS'].keys():
                    continue

                # Mark the object
                child['CELSTE_RIG_OBJ_ID'] = master_bone['CELSTE_RIG_ID']

                # create the custom properties
                master_key_n = f'CELSTE_{m_type}_PVAR_N'
                master_key_t = f'CELSTE_{m_type}_PVAR_T'
                master_key_v = f'CELSTE_{m_type}_PVAR_V'
                if m_type not in data.keys():
                    data[m_type] = self.settings['PERF_MODIFIERS'][m_type]
                    master_bone[master_key_n] = data[m_type]['name']
                    master_bone[master_key_t] = data[m_type]['def_active']
                    master_bone[master_key_v] = data[m_type]['def_value']

                # make custom property names usable for drivers
                master_key_t = f'pose.bones["{master_bone.name}"]["{master_key_t}"]'
                master_key_v = f'pose.bones["{master_bone.name}"]["{master_key_v}"]'

                # add drivers
                m.driver_remove('show_viewport')
                d = self.add_driver(source=m, target=obj, prop='show_viewport', dataPath=master_key_t)
                data[m_type]['drivers'].append({'driver': d, 'prop': 'show_viewport', 'obj': child})
                if 'prop' in data[m_type].keys():
                    m.driver_remove(data[m_type]['prop'])
                    d = self.add_driver(source=m, target=obj, prop=data[m_type]['prop'], dataPath=master_key_v)
                    print(d, type(d))
                    data[m_type]['drivers'].append({'driver': d, 'offset': 0, 'prop': data[m_type]['prop'], 'obj': child})

            # update drivers
            for d in child.animation_data.drivers:
                d.driver.expression += ' '
                d.driver.expression = d.driver.expression[:-1]

        # update perf data
        master_bone['PERF_CONFIG'] = data

        return { 'FINISHED' }
class PerfVarEditFinish     (Classes.CelsteOperator):
    bl_idname = 'opr.perf_var_edit_finish_operator'
    bl_label = 'Finish'
    bl_description = 'Finish editing the performance vars.'

    def execute(self, context):
        verify = self.verify_selection(context)
        if verify == None:
            return { 'CANCELLED' }

        arm, master_bone = verify
        data = master_bone['PERF_CONFIG']
                        
        for key in data.to_dict().keys():   
            for m in data[key]['drivers']:
                # m = m.to_dict()
                print('m:', m.items())
                print('m:', m.values())
                print('d:', m['driver'], type(m['driver']))
                # try:
                #     m['driver'].expression = m['prop'] + ' + ' + str(m['offset'])
                # except KeyError:
                #     m['driver'].expression = m['prop']

        return { 'FINISHED' }


# Performane Var Operators
class SUBSURF_ActiveOperator (Classes.CustomBoolProp):
    modifier_id = 'SUBSURF' # Change this value if adding new Perf Vars

    bl_idname = f'opr.{modifier_id.lower()}_active_operator'
    bl_label = modifier_id
    bl_description = f'Toggle {modifier_id} active state.'

    def __init__(self) -> None:
        super().__init__()
        self.obj = self.verify_selection(bpy.context)[1]
        self.prop = f'CELSTE_{self.modifier_id}_PVAR_T'

    def execute(self, context):
        super().execute(context)
        mode = context.object.mode
        if mode == 'EDIT':
            bpy.ops.object.mode_set()
            bpy.ops.object.mode_set(mode=mode)
        else:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.mode_set(mode=mode)

        return { 'FINISHED' }
class SMOOTH_ActiveOperator (Classes.CustomBoolProp):
    modifier_id = 'SMOOTH' # Change this value if adding new Perf Vars

    bl_idname = f'opr.{modifier_id.lower()}_active_operator'
    bl_label = modifier_id
    bl_description = f'Toggle {modifier_id} active state.'

    def __init__(self) -> None:
        super().__init__()
        self.obj = self.verify_selection(bpy.context)[1]
        self.prop = f'CELSTE_{self.modifier_id}_PVAR_T'

    def execute(self, context):
        super().execute(context)
        mode = context.object.mode
        if mode == 'EDIT':
            bpy.ops.object.mode_set()
            bpy.ops.object.mode_set(mode=mode)
        else:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.mode_set(mode=mode)

        return { 'FINISHED' }


LAYER_CLASSES = [
    LastLayerOperator,
    NextLayerOperator,
    LayerUpOperator,
    LayerDownOperator,
    LayerDeleteOperator,
    LayerAddOperator,
    BoxDeleteOperator,
    BoxAddOperator,
    StartRigEditOperator,
    FinishRigEditOperator,
]

PERF_CLASSES = [
    PerfVarConfig,
    PerfVarEditFinish,
]

PERF_OPERATORS = [
    SUBSURF_ActiveOperator,
    SMOOTH_ActiveOperator,
]

CLASSES = [
    RigEditPanel,
    *LAYER_CLASSES,
    *PERF_CLASSES,
    *PERF_OPERATORS,
]   



