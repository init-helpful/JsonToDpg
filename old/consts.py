import dearpygui.dearpygui as dpg

regex_list = "\[.*\]"
function_substring_filters = ["add_", "create_"]
other_functions = ["configure_app"]
KEY_SPLIT_CHAR = "->"
WINDOW = "window"
ARGS = "args"
TAG = "tag"
FUNCTION_REFERENCE = "function_reference"
BRANCH_LEVEL_IDENTIFIER = "-"
ID = "tag"
LEVEL = "level"
PARENT = "parent"
ADD_WINDOW = "add_window"
KEY_SPLIT_CHAR = "."
__all__ = [
    "ADD_WINDOW",
    "ARGS",
    "BRANCH_LEVEL_IDENTIFIER",
    "FUNCTION_REFERENCE",
    "ID",
    "KEY_SPLIT_CHAR",
    "LEVEL",
    "PARENT",
    "TAG",
    "WINDOW",
    "function_substring_filters",
    "other_functions",
    "regex_list",
    'dpg'
]

if __name__ == "__main__":
    from allmaker import AllMaker

    AllMaker().print_all("consts")