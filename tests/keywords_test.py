from testsetup import setup_pathing

setup_pathing()

from jsontodpg import JsonToDpg
from dpgkeywords import *

# --- Step 1: Initialize the library. ---
# The constructor will now automatically check and regenerate dpgkeywords.py
# in the background if it's missing or out of date.
jtd = JsonToDpg()

# --- Step 2: Create a convenience alias for the keyword accessor. ---
# Your script will ALWAYS use this. It works immediately, even if the
# keyword file didn't exist a moment ago.
k = jtd.keywords

# --- Step 3: Define the UI using the keyword accessor. ---
main_ui = {
    # SETUP PHASE:
    "setup_calls": [
        {put: ["message", "Hello, Self-Generating Keywords!"]},
        {add_monitor: ["message", "monitored_text"]},
    ],
    viewport: {width: 800, height: 400, title: "Automatic Keyword System Test"},
    window: {
        label: "Automatic Keyword Demo",
        width: 780,
        height: 380,
        "children": [
            {
                text: {
                    default_value: "This script automatically generated dpgkeywords.py."
                }
            },
            {text: {default_value: "Your IDE will now have code completion for '*'."}},
            {separator: {}},
            {
                group: {
                    horizontal: True,
                    "items": [
                        {text: {default_value: "Monitored Text:"}},
                        {text: {tag: "monitored_text"}},
                    ],
                }
            },
            {
                button: {
                    label: "Update store via 'put' keyword",
                    callback: {put: ["message", "Store updated successfully!"]},
                }
            },
        ],
    },
}

# --- Step 4: Start the application. ---
jtd.start(main_ui)
