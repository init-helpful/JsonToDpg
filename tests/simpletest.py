from testsetup import setup_pathing

setup_pathing()

from jsontodpg import JsonToDpg
from dpgkeywords import *

j_to_dpg = JsonToDpg(generate_keyword_file_name=False, debug=False)
c = j_to_dpg.controller

main = {
    viewport: {width: 800, height: 600},
    window: {
        label: "Example Window",
        width: 400,
        height: 300,
        pos: [200, 150],
        input_text: {default_value: "Enter some text", tag: "input_to_print"},
        button: {
            label: "Submit",
            callback: lambda: print(c.get_value("input_to_print")),
        },
    },
}

j_to_dpg.start(main)
