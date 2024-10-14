from tokenizer import Tokenizer
from asyncfunction import AsyncFunction
from dpgkeywords import *
from controller import Controller
import dearpygui.dearpygui as dpg
import dpgextended as dpg_extended
# from threading import Thread

FUNCTION_NAME = "name"
REFERENCE = "function reference"
ARGS = "args"
IS_PLUGIN = "is_plugin"
LEVEL = "level"
PARENT = "parent"
TAG = "tag"
MAX_TICK = 86400  # 24 Hours In Seconds

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


class JsonToDpg:
    def __init__(
        self,
        generate_keyword_file_name="",
        debug=False,
        async_functions={},
        plugins=[],
    ):
        self.dpg = dpg
        self.parse_history = []
        self.debug = debug
        self.async_functions = async_functions
        self.tokenizer = Tokenizer(
            dpg=self.dpg,
            generate_keyword_file_name=generate_keyword_file_name,
            plugins=[dpg_extended] + (plugins if plugins else []),
        )
        self.canceled_asycn_functions = (
            []
        )  # Store for funcitons that have been canceled
        self.__is_debug(debug)
        self.reversed_stack = []
        self.controller = Controller(self)

    def __is_debug(self, debug):
        if debug:
            dpg.show_metrics()

    def add_async_function(
        self, interval, function, end_condition=None, pause_condition=None, num_cycles=0
    ):
        if not interval in self.async_functions:
            self.async_functions[interval] = []
        self.async_functions[interval].append(
            AsyncFunction(
                interval, function, end_condition, pause_condition, num_cycles
            )
        )

    def __build_and_run(self, json_object):
        self.build_function_stack(json_object)

        for function in self.function_stack:

            if self.debug:
                print(f"Current function: {function[FUNCTION_NAME]}")
                print(f"Arguments: {function[ARGS]}")
                print()

            function[REFERENCE](**function[ARGS])

    def object_already_exists(self, d):
        existing_tags = set(dpg.get_aliases())

        def check_item(item):
            if item in existing_tags:
                self.dpg.show_item(item)
                self.dpg.focus_item(item)
                return True

            if isinstance(item, dict):
                for value in item.values():
                    if check_item(value):
                        return True
            elif isinstance(item, list):
                for subitem in item:
                    if check_item(subitem):
                        return True

            return False

        if isinstance(d, dict):
            for value in d.values():
                if check_item(value):
                    return True
        elif isinstance(d, list):
            for item in d:
                if check_item(item):
                    return True

        return False

    def parse(self, json_object, check_for_existing=False):
        self.existing_tags = self.dpg.get_aliases()
        if not (check_for_existing and self.object_already_exists(json_object)):
            self.function_stack = []
            self.parse_history.append(json_object)
            self.__build_and_run(json_object)

    def __remove_canceled_async_functions(self):
        for interval_and_index in self.canceled_asycn_functions:
            del self.async_functions[interval_and_index[0]][interval_and_index[1]]

    def __run_async_functions(self, ticks):
        self.__remove_canceled_async_functions()
        self.canceled_asycn_functions = []
        for interval, function_set in self.async_functions.items():
            if ticks % interval == 0:
                for function_index, function in enumerate(function_set):
                    if function.end_condition() or (
                        function.cycles and function.times_performed >= function.cycles
                    ):
                        self.canceled_asycn_functions.append([interval, function_index])
                    if not function.pause_condition():
                        function.run()
                    function.times_performed += 1

    def __start_async_loop(self):
        ticks = 0

        while dpg.is_dearpygui_running():
            ticks += 1
            self.dpg.render_dearpygui_frame()
            self.__run_async_functions(ticks)
            # Thread(target=self.__run_async_functions, args=[ticks]).start()
            if ticks > MAX_TICK:
                ticks = 0
        dpg.stop_dearpygui()

    def start(self, json_object):
        self.function_stack = []
        dpg.create_context()
        self.parse(json_object)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        self.__start_async_loop()
        dpg.destroy_context()

    def _reverse_stack(self):
        self.reversed_stack = reversed(self.function_stack)

    def get_parent(self, current_level, stack=None):
        if not stack:
            stack = self.function_stack
        self._reverse_stack()

        try:
            return next(
                item[TAG]
                for item in self.reversed_stack
                if item[LEVEL] < current_level
                and item[FUNCTION_NAME] not in PARENT_IGNORE_LIST
            )
        except StopIteration:
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
