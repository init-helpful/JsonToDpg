from re import I
import dearpygui.dearpygui as dpg
from collections import OrderedDict

COMPONENT_IDENTIFIERS_REMOVE_SUB = ["add_", "create_"]
COMPONENT_IDENTIFIERS_KEEP_SUB = ["draw"]
SHARED_PYTHON_KEYWORDS = ["format"]


def clean_keyword(current_item):
    if current_item[0].isnumeric() or current_item in SHARED_PYTHON_KEYWORDS:
        return f"_{current_item}"
    return current_item


def clean_keywords_list(_list):
    for i in range(len(_list)):
        _list[i] = clean_keyword(_list[i])
    return _list


def remove_quotes(obj):
    return str(obj).replace('"', "").replace("'", "")


def write_to_py_file(file_path="", file_name="generated_python_file", data=""):
    temp_path = file_path + file_name + ".py"
    with open(temp_path, "w") as f:
        f.write(data)


def check_for_substrings(string, comparison_list, return_diff=False):
    for sub in comparison_list:
        if sub in string:
            if return_diff:
                return string.replace(sub, "")
            return string


class Tokenizer:
    def __init__(self, save_to_file=False):
        # Which parameters can be used with each
        self.component_parameter_relations = OrderedDict()
        self.components = {}
        self.parameters = []
        # ---------------------------
        self.build_keyword_library()
        if save_to_file:
            self.write_to_file()

    def build_keyword_library(self):
        
        for function_name in dir(dpg):
            clipped_keyword = check_for_substrings(
                function_name, COMPONENT_IDENTIFIERS_REMOVE_SUB, return_diff=True
            )
            if not clipped_keyword:
                clipped_keyword = check_for_substrings(
                    function_name, COMPONENT_IDENTIFIERS_KEEP_SUB
                )

            if clipped_keyword:
                clipped_keyword = clean_keyword(clipped_keyword)
                function_reference = getattr(dpg, function_name)

                self.components[clipped_keyword] = function_reference

                params = clean_keywords_list(
                    [
                        param
                        for param in function_reference.__code__.co_varnames
                        if not param in ["args", "kwargs"]
                    ]
                )

                # Add non-existing parameters to master parameter list
                self.parameters = self.parameters + [
                    param for param in params if not param in self.parameters
                ]

                self.component_parameter_relations[clipped_keyword] = params

    def write_to_file(self):
        string = "#THIS FILE WAS GENERATED\n"
        components = list(self.components.keys())

        string = (
            string + f"#--------------COMPONENTS--------------[{len(components)}]\n"
        )

        for component in components:
            string = string + "\n" + f'{component}="{component}"'

        string = (
            string
            + "\n"
            + f"\n#--------------PARAMETERS--------------[{len(self.parameters)}]\n"
        )

        for param in self.parameters:
            string = string + "\n" + f'{param}="{param}"'

        string = (
            string
            + "\n\n"
            + f"component_parameter_relations = {remove_quotes(str(dict(self.component_parameter_relations)))}"
        )
        string = string + "\n" + f"__all__ = {components + self.parameters}"

        write_to_py_file(file_name="dpgkeywords", data=string)
