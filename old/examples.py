
from dpgtojson import JsonToDpg
from keywords import *
import dearpygui.dearpygui as dpg

VIEW_HEIGHT = 1200
VIEW_WIDTH = 1200


def test():
    
    return [
        {button: {"label": "save1"}},
        {button: {"label": "test2"}},
        {button: {"label": "test3000"}},
    ]
     

table_window = {
    "label": "Table Window",
    "pos": str([0,0]),
    "width": VIEW_WIDTH / 2,
    "height": VIEW_HEIGHT,

}

standard_window = {
    "label": "Another Window",
    "pos": str([int(VIEW_WIDTH / 2), 0]),
    "width": VIEW_WIDTH / 2,
    "height": VIEW_HEIGHT,
    text: {"default_value": "Hello, World"},
    input_text: {"default_value": "Quick brown fox"},
    slider_float: {
        "default_value": 0.273,
        "max_value": 1,
    },
    "buttons": test(),
    "other_buttons": [
        {button: {"label": "save1"}},
        {button: {"label": "test2"}},
        {button: {"label": "test3"}},
    ],
}

multi_window_example = {
    "viewport": {
        "title": "Multi Window Example",
        "width": VIEW_HEIGHT,
        "height": VIEW_HEIGHT,
    },
    "configure_app": {"docking": True, "docking_space": True},
    "standard_window": standard_window,
    "table_window": table_window,
}

if __name__ == "__main__":
    JsonToDpg().parse(multi_window_example)