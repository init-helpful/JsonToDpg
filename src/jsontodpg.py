from tokenizer import Tokenizer
from dpgkeywords import *
import dearpygui.dearpygui as dpg

FUNCTION_NAME = "name"
REFERENCE = "function reference"
ARGS = "args"
LEVEL = "level"
PARENT = "parent"
TAG = "tag"

PARENT_IGNORE_LIST = [viewport, input_text]


def children(obj):
    """
    Iterate through and find child objects from input collection

    Args:
        obj (tuple,dict,list): the parent object.

    Returns:
        Children collections of input collection if they are tuple, dict or list.
    """

    collection_types = {
        "tuple": lambda obj: obj,
        "list": lambda obj: obj,
        "dict": lambda obj: obj.items(),
    }

    return [
        item
        for item in collection_types[type(obj).__name__](obj)
        if type(item).__name__ in collection_types
    ]


class AsyncFunction:
    def __init__(self, interval, function_reference, end_condition=None, cycles=0):
        self.interval = interval
        self.function_reference = function_reference
        self.cycles = cycles
        self.times_performed = 0
        self.end_condition = end_condition

    def run(self):
        self.function_reference()


class JsonToDpg:
    def __init__(
        self,
        generate_keyword_file_name="",
        use_dpg_extended=True,
        debug=False,
        async_functions=[],
    ):
        self.dpg = dpg
        self.parse_history = []
        self.debug = debug
        self.async_functions = async_functions
        self.tokenizer = Tokenizer(
            generate_keyword_file_name=generate_keyword_file_name,
            use_dpg_extended=use_dpg_extended,
        )

    def add_async_function(
        self, interval, function, end_condition=None, num_cycles=0
    ):
        if not interval in self.async_functions:
            self.async_functions[interval] = []
        self.async_functions[interval].append(
            AsyncFunction(interval, function, end_condition, num_cycles)
        )

    def __build_and_run(self, json_object):
        self.build_function_stack(json_object)

        for function in self.function_stack:
            if self.debug:
                print(function)
            function[REFERENCE](**function[ARGS])

    def object_already_exists(self, d):
        if isinstance(d, dict):
            for value in d.values():
                if value in self.existing_tags:
                    self.dpg.show_item(value)
                    self.dpg.focus_item(value)
                    return True
                if isinstance(value, (dict, list)):
                    return self.object_already_exists(value)

        elif isinstance(d, list):
            for item in d:
                if isinstance(item, (dict, list)):
                    return self.object_already_exists(item)

        return False

    def parse(self, json_object, check_for_existing=False):
        self.existing_tags = self.dpg.get_aliases()
        if not (check_for_existing and self.object_already_exists(json_object)):
            self.function_stack = []
            self.parse_history.append(json_object)
            self.__build_and_run(json_object)

    def __remove_from_async_functions(self, functions_to_remove=[]):
        for interval_and_index in functions_to_remove:
            del self.async_functions[interval_and_index[0]][interval_and_index[1]]

    def __start_async_loop(self):
        ticks = 0
        functions_to_remove_before_next_pass = []

        while dpg.is_dearpygui_running():
            self.__remove_from_async_functions(functions_to_remove_before_next_pass)
            functions_to_remove_before_next_pass = []
            ticks += 1
            for interval, function_set in self.async_functions.items():
                if ticks % interval == 0:
                    for function_index, function_to_perform in enumerate(function_set):
                        run_this = True

                        if (
                            function_to_perform.end_condition
                            and function_to_perform.end_condition()
                        ):
                            run_this = False

                        if (
                            function_to_perform.cycles
                            and function_to_perform.times_performed
                            >= function_to_perform.cycles
                        ):
                            run_this = False

                        if run_this:
                            function_to_perform.run()
                            function_to_perform.times_performed += 1
                        else:
                            functions_to_remove_before_next_pass.append(
                                [interval, function_index]
                            )

            dpg.render_dearpygui_frame()
        dpg.stop_dearpygui()

    def start(self, json_object):
        self.function_stack = []
        dpg.create_context()
        self.parse(json_object)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        self.__start_async_loop()
        dpg.destroy_context()

    def get_parent(self, current_level):
        reverse_call_stack = self.function_stack[::-1]
        for i in range(len(reverse_call_stack)):
            last_item = reverse_call_stack[i]
            if (
                last_item[LEVEL] < current_level
                and not last_item[FUNCTION_NAME] in PARENT_IGNORE_LIST
            ):
                return last_item[ARGS][TAG]
        return ""

    def build_function_stack(self, _object, level=0):
        # Reset call stack if somehow there is residual calls
        if level == 0:
            self.function_stack = []

        # Find Tuples, Dicts, and Lists in current object
        children_objects = children(_object)

        if isinstance(_object, tuple):
            object_name = _object[0]

            # Is Recognized Function
            if object_name in self.tokenizer.components:
                tag_name = f"{len(self.parse_history)}-{len(self.function_stack)}-{object_name}"
                self.__add_function_to_stack(object_name, level, tag_name)
                self.__assign_parent_and_tag(object_name, level, tag_name)

            # Is Recognized Parameter Of Function
            elif object_name in self.tokenizer.parameters:
                self.function_stack[-1][ARGS].update({object_name: _object[1]})

        # Dig into Tuples, Dicts, and Lists. Increment Level. Start Again.
        for child in children_objects:
            self.build_function_stack(_object=child, level=level + 1)

    def __add_function_to_stack(self, object_name, level, tag_name):
        self.function_stack.append(
            (
                {
                    FUNCTION_NAME: object_name,
                    REFERENCE: self.tokenizer.components[object_name],
                    TAG: tag_name,
                    LEVEL: level,
                    ARGS: {},
                }
            )
        )

    def __assign_parent_and_tag(self, object_name, level, tag_name):
        if PARENT in self.tokenizer.component_parameter_relations[object_name]:
            parent = self.get_parent(level)
            if parent:
                self.function_stack[-1][ARGS].update({PARENT: parent})
        if TAG in self.tokenizer.component_parameter_relations[object_name]:
            self.function_stack[-1][ARGS].update({TAG: tag_name})