import bpy
import json
from sys import path
import os


class CelstePanel(bpy.types.Panel):
    def __init__(self) -> None:
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.settings = json.load(open(__location__ + '\\settings.json'))

    def verify_selection(self, context):
        obj = context.object
        if type(obj) != None and obj.type == 'ARMATURE':
            for bone in obj.pose.bones:
                for prop in bone.items():
                    if prop[0] == 'CELSTE_RIG_ID':
                        return (obj.data, bone)
        return None

    def add_driver(
            source, target, prop, dataPath,
            index = -1, negative = False, func = ''
        ):
        ''' Add driver to source prop (at index), driven by target dataPath '''

        if index != -1:
            d = source.driver_add( prop, index ).driver
        else:
            d = source.driver_add( prop ).driver

        v = d.variables.new()
        v.name                 = prop
        v.targets[0].id        = target
        v.targets[0].data_path = dataPath

        d.expression = func + "(" + v.name + ")" if func else v.name
        d.expression = d.expression if not negative else "-1 * " + d.expression

class CelsteOperator(bpy.types.Operator):
    def __init__(self) -> None:
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.settings = json.load(open(__location__ + '\\settings.json'))
        self.pull_data = 'CONVERT_DATA'

    def verify_selection(self, context):
        obj = context.object
        if type(obj) != None and obj.type == 'ARMATURE':
            for bone in obj.pose.bones:
                for prop in bone.items():
                    if prop[0] == 'CELSTE_RIG_ID':
                        return (obj.data, bone)
        return None

    def add_driver(self,
            source, target, prop, dataPath, targetType = 'OBJECT',
            index = -1, negative = False, func = ''
        ):
        ''' Add driver to source prop (at index), driven by target dataPath '''

        if index != -1:
            d = source.driver_add( prop, index ).driver
        else:
            d = source.driver_add( prop ).driver

        v = d.variables.new()
        v.name                 = prop
        v.targets[0].id_type   = targetType
        v.targets[0].id        = target
        v.targets[0].data_path = dataPath

        d.expression = func + "(" + v.name + ")" if func else v.name
        d.expression = d.expression if not negative else "-1 * " + d.expression

        return d

class CustomBoolProp(CelsteOperator):
    bl_idname = 'opr.change_bool_prop'
    bl_label = 'Change Bool'
    bl_description = 'Toggle the value of a Custom Property as if it was a bool'

    def __init__(self) -> None:
        super().__init__()
        self.obj = bpy.context.object
        self.prop = 'prop'

    def execute(self, context):
        if self.obj[self.prop] == 0:
            self.obj[self.prop] = 1
        else:
            self.obj[self.prop] = 0

        try:
            self.obj.update_tag()
        except AttributeError:
            context.object.update_tag()

CLASSES = [
    CelstePanel,
    CelsteOperator,
    CustomBoolProp,
]
