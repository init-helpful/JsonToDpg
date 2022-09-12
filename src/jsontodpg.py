from tokenizer import Tokenizer
from dpgkeywords import *
import dearpygui.dearpygui as dpg

FUNCTION_NAME = "name"
FUNCTION_REF = "function reference"
ARGS = "args"
LEVEL = "level"
PARENT = "parent"
TAG = "tag"


def children(obj):
    children_objects = []
    children_variables = []

    object_types = {
        "tuple": lambda obj: obj,
        "dict": lambda obj: obj.items(),
        "list": lambda obj: obj,
    }

    for x in object_types[type(obj).__name__](obj):
        if type(x).__name__ in object_types:
            children_objects.append(x)
        else:
            children_variables.append(x)

    return children_objects


class JsonToDpg:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.call_stack = []

    def run(self, json_object):
        self.build(json_object)

        for function_call in self.call_stack:
            reference = function_call[FUNCTION_REF]
            args = function_call[ARGS]
            reference(**args)

    def parse(self, json_object):
        dpg.create_context()
        self.run(json_object)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def get_parent(self, current_level):
        reverse_call_stack = self.call_stack[::-1]
        for i in range(len(reverse_call_stack)):
            last_item = reverse_call_stack[i]
            if (
                last_item[LEVEL] < current_level
                and not last_item[FUNCTION_NAME] == "viewport"
            ):
                return last_item[TAG]
        return ""

    def build(self, _object, level_num=0):

        # Reset Call stack if somehow there is residual calls
        if level_num == 0:
            self.call_stack = []

        children_objects = children(_object)

        if isinstance(_object, tuple):
            object_lead = _object[0]

            if object_lead in self.tokenizer.components:

                tag_name = f"{len(self.call_stack)}-{object_lead}"
                self.call_stack.append(
                    (
                        {
                            FUNCTION_NAME: object_lead,
                            FUNCTION_REF: self.tokenizer.components[object_lead],
                            TAG: tag_name,
                            LEVEL: level_num,
                            ARGS: {},
                        }
                    )
                )
                if not object_lead == viewport:
                    parent = self.get_parent(level_num)
                    if parent:
                        self.call_stack[-1][ARGS].update({PARENT: parent})
                    self.call_stack[-1][ARGS].update({TAG: tag_name})

            elif object_lead in self.tokenizer.parameters:
                if object_lead == TAG:
                    self.call_stack[-1][TAG] = _object[1]
                self.call_stack[-1][ARGS].update({object_lead: _object[1]})

        for child in children_objects:
            self.build(_object=child, level_num=level_num + 1)
