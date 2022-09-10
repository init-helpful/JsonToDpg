import dearpygui.dearpygui as dpg
from collections import OrderedDict

COMPONENT_IDENTIFIERS = ["add_", "create_"]
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


def write_to_py_file(
    file_path="Generated/", file_name="generated_python_file", data=""
):
    temp_path = file_path + file_name + ".py"
    with open(temp_path, "w") as f:
        f.write(data)


def check_for_substrings(string, comparison_list, return_diff=True):
    for sub in comparison_list:
        if sub in string:
            if return_diff:
                return string.replace(sub, "")
            return sub


class Tokenizer:
    def __init__(self, write_to_file=False):
        self.component_parameter_relations = OrderedDict()
        self.function_references = {}
        # ---------------------------
        self.build_keyword_library()
        self.write_to_file()

    def build_keyword_library(self):
        for function_name in dir(dpg):
            clipped_keyword = check_for_substrings(function_name, COMPONENT_IDENTIFIERS)

            if clipped_keyword:
                clipped_keyword = clean_keyword(clipped_keyword)
                function_reference = getattr(dpg, function_name)

                self.function_references[clipped_keyword] = function_reference

                self.component_parameter_relations[
                    clipped_keyword
                ] = clean_keywords_list(
                    [
                        param
                        for param in function_reference.__code__.co_varnames
                        if not param in ["args", "kwargs"]
                    ]
                )

    def get_parameters(self):
        self.parameters = []

        for parameter_sets in self.component_parameter_relations.values():
            for param in parameter_sets:
                if param not in self.parameters:
                    self.parameters.append(param)

        self.parameters.sort()

        return self.parameters

    def write_to_file(self):
        string = ""
        components = list(self.component_parameter_relations.keys())

        string = (
            string + f"#--------------COMPONENTS--------------[{len(components)}]\n"
        )

        for component in components:
            string = string + "\n" + f'{component}="{component}"'

        self.get_parameters()

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

        write_to_py_file(file_name="keywords", data=string)


Tokenizer()
