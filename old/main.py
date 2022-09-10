from jsontodpg import JsonToDpg
from keywords import *
from consts import dpg

VIEW_HEIGHT = 1200
VIEW_WIDTH = 1200


connection_window = {
    "label": "Another Window",
    "pos": str([0, 0]),
    "width": VIEW_WIDTH / 2,
    "height": VIEW_HEIGHT / 4,
    text: {"default_value": "Hello, World"},
    input_text: {"default_value": "Quick brown fox", "multiline": True},
}


connection_window = {
    "label": "Another Window",
    "pos": str([0, 0]),
    "width": VIEW_WIDTH / 2,
    "height": VIEW_HEIGHT / 4,
    
    
    "c":[{tab_bar:{'label':'t',"children":[{"tab_button":{}}]}},{tab_bar:{'label':'t2'}}]
    
    # tab_bar: {
    #     "label": "test",
    #     "BUTTONS": [{tab_button: {"label": "test"}}, {tab_button: {"label": "test2"}}],
    # }
    
    # text: {"default_value": "Hello, World"},
    # input_text: {"default_value": "Quick brown fox", "multiline":True},
}


main = {
    "viewport": {
        "title": "Multi Window Example",
        "width": VIEW_HEIGHT,
        "height": VIEW_HEIGHT,
    },
    "connection_window": connection_window,
}


if __name__ == "__main__":
    JsonToDpg().parse(main)
