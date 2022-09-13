

from src.jsontodpg import JsonToDpg
from src.dpgkeywords import *

window_1 = {window: {label: "Example Window 1", width: 400, height: 400, pos: [0, 0]}}
window_2 = {window: {label: "Example Window 2", width: 400, height: 400}, pos: [400, 0]}
window_3 = {window: {label: "Example Window 3", width: 400, height: 400}, pos: [0, 400]}
window_4 = {
    window: {label: "Example Window 4", width: 400, height: 400},
    pos: [400, 400],
}


main = {
    viewport: {width: 800, height: 800},
    "t ": [
        window_1,
        window_2,
        window_3,
        window_4,
    ],

}

JsonToDpg().build(main)