import re
from consts import *
from utils import (
    flatten,
    build_function_lookup,
    count_numeric_values,
    find_parent_path,
    list_difference,
    remove_non_matching,
)


class JsonToDpg:
    def __init__(self):
        self.recognized_functions = build_function_lookup()

    def lookup_function(self, item, index, level, value=None):
        item_id = f"{item}-{index}"
        function_data = {ARGS: {TAG: item_id}, FUNCTION_REFERENCE: None, LEVEL: level}
        if WINDOW in item:
            function_data[FUNCTION_REFERENCE] = self.recognized_functions[WINDOW]

        elif item in self.recognized_functions:
            function_data[FUNCTION_REFERENCE] = self.recognized_functions[item]

        elif value and callable(value):
            function_data[FUNCTION_REFERENCE] = value

        return function_data

    def find_parent_function(self, level, function_stack, child_is_custom=False):
        previous_functions = function_stack[::-1]

        if not child_is_custom:
            for function in previous_functions:
                if function[LEVEL] < level or function[LEVEL] == 0:
                    return function[ARGS][TAG]
        else:
            for function in previous_functions:
                if (
                    function[LEVEL] == level
                    or function[LEVEL] == 0
                    and function[FUNCTION_REFERENCE].__name__
                    not in self.recognized_functions
                ):
                    return function[ARGS][TAG]

    def generate_item_stack(self, path_keys):

        item_stack = []
        item_stack_with_level = []
        for path_idx, path in enumerate(path_keys):
            items_to_add = []
            current_path = path.split(KEY_SPLIT_CHAR)
            numeric_count = count_numeric_values(current_path)
            level = len(current_path) - 2 - numeric_count
            parent_path = find_parent_path(current_path, level, path_keys[:path_idx])

            # If is root object
            if path_idx == 0 or current_path[0] not in item_stack:
                items_to_add = current_path
                
            # Or Has parent of lower level
            elif parent_path:
                
                items_to_add = list_difference(parent_path, current_path)

            # Has parent of equal level
            else:
                
                items_to_add = list_difference(
                    path_keys[path_idx - 1].split(KEY_SPLIT_CHAR), current_path
                )

        
            if numeric_count and items_to_add:
                items_to_add.pop(0)

            item_stack.extend(items_to_add)
            item_stack_with_level.extend([f"{x}:{level}" for x in items_to_add])

        return item_stack_with_level

    def build_function_stack(self, item_stack, path_values):
        function_stack = []

        for item_index, item in enumerate(item_stack):

            item, level = item.split(":")
            if not item.isnumeric():
                if path_values:

                    found_function = self.lookup_function(
                        item, item_index, level, path_values[0]
                    )
                else:
                    found_function = self.lookup_function(item, item_index, level)

                if found_function[FUNCTION_REFERENCE]:

                    if function_stack and int(level) > 0:

                        if item in self.recognized_functions:
                            parent = self.find_parent_function(level, function_stack)

                        else:

                            parent = self.find_parent_function(
                                level, function_stack, child_is_custom=True
                            )

                        found_function[ARGS].update({PARENT: parent})

                    function_stack.append(found_function)

                else:

                    if path_values:
                        function_stack[-1][ARGS].update({item: path_values.pop(0)})

        return function_stack

    def post_process_values(self, args):
        updated_args = {}
        for key, value in args.items():
            if value not in ["", [], {}]:
                if isinstance(value, str) and re.match("\[.*\]", value):
                    list_object = [
                        int(item.replace("[", "").replace("]", ""))
                        for item in value.split(",")
                        if item not in ["[", "]"]
                    ]
                    updated_args[key] = list_object
                else:
                    updated_args[key] = value
        return updated_args

    def perform_function_stack(self, function_stack):

        for function_call in function_stack:
            reference = function_call[FUNCTION_REFERENCE]

            args = function_call[ARGS]

            args = pre = self.post_process_values(args)

            params = reference.__code__.co_varnames
            if reference.__name__ not in other_functions:
                args = remove_non_matching(args, params)

                reference(**args)

    def __build_ui_without_boiler_plate(self, function_stack):
        dpg.create_context()
        self.perform_function_stack(function_stack)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def __print_function_lookup(self):
        for k, v in self.recognized_functions.items():
            print(k + " = " + "'" + k + "'" + " #" + v.__name__)

    def parse(self, dictionary):
        paths = flatten(dictionary)
        item_stack = self.generate_item_stack(list(paths.keys()))

        function_stack = self.build_function_stack(item_stack, list(paths.values()))
        # pl(item_stack)

        self.__build_ui_without_boiler_plate(function_stack=function_stack)


if __name__ == "__main__":
    from examples import multi_window_example

    j = JsonToDpg()
    j.parse(multi_window_example)
