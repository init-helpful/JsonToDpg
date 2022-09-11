from tokenizer import Tokenizer
from keywords import *

FUNCTION_NAME = "function name"
FUNCTION_REF = "function reference"
ARGS = "args"


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

    return children_objects, children_variables


class JsonToDpgTranslator:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.call_stack = []

    def run(self, json_object):
        self.build(json_object)
        [print(x) for x in self.call_stack]

    def add_to_call_stack(self, function):
        pass

    def build(self, _object, level_num=0, _previous=None):
        # Reset Call stack if somehow there is residual calls
        if level_num == 0:
            self.call_stack = []

        children_objects, children_variables = children(_object)

        if isinstance(_object, tuple):
            object_lead = _object[0]

            if object_lead in self.tokenizer.components:
                self.call_stack.append(
                    (
                        {
                            FUNCTION_REF: self.tokenizer.components[object_lead],
                            FUNCTION_NAME: object_lead,
                            ARGS: {},
                        }
                    )
                )
            if object_lead in self.tokenizer.parameters:
                self.call_stack[-1][ARGS].update({object_lead:_object[1]})

        for child in children_objects:
            self.build(_object=child, level_num=level_num + 1, _previous=_object)


test = {
    viewport: {
        title: "Multi Window Example",
        width: 100,
        height: 100,
    },
    "windows": [
        {
            window: 
                {
                    label: "test window",
                    width: 100,
                    height: 100,
                    pos: [100 / 2, 0],
                    text: {default_value : "Hello, World"},
                    input_text: {default_value: "Quick brown fox"},
                }
        },
        
        
        
        # {window: {label: "test window5", width: 100, height: 100, pos: [100 / 2, 0]}},
    ],
}


JsonToDpgTranslator().run(test)
