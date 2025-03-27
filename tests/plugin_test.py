from testsetup import setup_pathing
import random

setup_pathing()

import plugin

from dpgkeywords import *
from jsontodpg import JsonToDpg


j_to_dpg = JsonToDpg(generate_keyword_file_name="test.py",plugins=[plugin] ,debug=False)
c = j_to_dpg.controller

c.put("default_width", 400)
c.put("default_height", 400)


def gen_and_store_random_number():
    # Generate a random integer between 1 and 100
    random_integer = random.randint(1, 10000000000000)
    c.put("random_integer", random_integer)
    # print(j_to_dpg.models)

def get_random_number():
    c.set_value("number_input", c.get("random_integer"))


def windows():
    return [
        {
            
            window: {
                "test_func":{},
                "gen_random_number": c.add_async_function(
                    interval=20, function=gen_and_store_random_number
                ),
                "get_random_number": c.add_async_function(
                    interval=20, function=get_random_number
                ),
                label: "Window 1",
                pos: [0, 0],
                width: c.get("default_width"),
                height: c.get("default_height"),
                button: {
                    "label": "Change Text",
                    tag: "BUTTON1",
                    callback: lambda: c.set_value(
                        tag="INPUT2", value=c.get_value("INPUT1")
                    ),
                },
                input_text: {default_value: "type here", tag: "INPUT1"},
            }
        },
        {
            window: {
                label: "Window 2",
                width: c.get("default_width"),
                height: c.get("default_height"),
                pos: [c.get("default_width"), 0],
                no_close: True,
                "inputs": [
                    {input_text: {tag: "INPUT2", default_value: "This Will Change"}},
                    {input_text: {default_value: "0", tag: "number_input"}},
                ],
            }
        },
    ]


main = {
    
    viewport: {width: 800, height: 400},
    # "setup": [{"controller.put": {"default_width": 400}}, {"controller.put": {"default_height": 400}}],
    "windows": windows(),
}

j_to_dpg.start(main)
