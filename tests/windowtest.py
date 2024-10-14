from testsetup import setup_pathing

setup_pathing()

from dpgkeywords import *
from jsontodpg import JsonToDpg


j_to_dpg = JsonToDpg(generate_keyword_file_name=False, debug=True)



window_1 = {
    window: {
        label: "Example Window 1",
        width: 400,
        height: 400,
        pos: [0, 0],
    },
}
window_2 = {window: {label: "Example Window 2", width: 400, height: 400}, pos: [400, 0]}
window_3 = {
    window: {
        width: 400,
        height: 400,
        pos: [0, 400],
    },
}
window_4 = {
    window: {label: "Example Window 4", width: 400, height: 400},
    pos: [400, 400],
}


main = {
    viewport: {width: 800, height: 800},
    "windows": [
        window_1,
        window_2,
        window_3,
        window_4,
    ],
}

j_to_dpg.start(main)