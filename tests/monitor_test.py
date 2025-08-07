from testsetup import setup_pathing

setup_pathing()

from jsontodpg import JsonToDpg


from dpgkeywords import *
import json


class StateMonitorPlugin:
    def __init__(self):
        self.controller = None

    def toggle_monitor(self, checkbox_tag, store_key, ui_tag):
        """Adds or removes a monitor based on the runtime state of a checkbox."""
        if not self.controller:
            return
        is_active = self.controller.get_value(checkbox_tag)
        if is_active:
            self.controller.add_monitor(store_key, ui_tag)
        else:
            self.controller.remove_monitor(store_key, ui_tag)

    def display_system_state(self, store_display_tag, monitors_display_tag):
        if not self.controller:
            return
        try:
            store_dict = self.controller.jsontodpg.model
            store_str = "--- Live Data Store ---\n" + json.dumps(
                store_dict, indent=2, default=str
            )
            if self.controller.component_exists(store_display_tag):
                self.controller.set_value(store_display_tag, store_str)
        except Exception as e:
            print(f"Error formatting store: {e}")

        try:
            monitors_dict = self.controller.monitors
            monitors_str = "--- Live Monitor Registry ---\n"
            if not monitors_dict:
                monitors_str += "(All monitors are disabled)"
            else:
                for key, monitors in monitors_dict.items():
                    monitors_str += f'"{key}": [\n'
                    for monitor_info in monitors:
                        monitors_str += f"    {{ tag: '{monitor_info['tag']}' }}\n"
                    monitors_str += "]\n"
            if self.controller.component_exists(monitors_display_tag):
                self.controller.set_value(monitors_display_tag, monitors_str)
        except Exception as e:
            print(f"Error formatting monitors: {e}")


# Regenerate the keyword file to include our new functions
j_to_dpg = JsonToDpg(plugins=[StateMonitorPlugin], debug=False)


main_ui = {
    "setup_calls": [
        {put: ["player_name", "Default User"]},
        {put: ["player_level", 50]},
        {put: ["is_premium", True]},
        {put: ["profile_color", [120, 150, 255, 255]]},
        {put: ["xp_boost", 1.5]},
        {add_monitor: ["player_name", "name_display"]},
        {add_monitor: ["player_level", "level_display"]},
        {add_monitor: ["is_premium", "premium_display"]},
        {add_monitor: ["profile_color", "color_display"]},
        {add_monitor: ["xp_boost", "boost_display"]},
        {
            add_async_function: {
                "args": [1],
                "kwargs": {
                    "function": {
                        "display_system_state": ["store_display", "monitors_display"]
                    },
                    "name": "SystemStateMonitor",
                },
            }
        },
    ],
    viewport: {width: 1000, height: 750, title: "Advanced Dynamic Monitor Test"},
    "input_window": {
        window: {
            label: "Input & Sync Control",
            width: 450,
            height: 700,
            pos: [10, 10],
            "input_window_controls": [
                {text: {default_value: "Toggle 'Sync' to enable/disable reactivity."}},
                {separator: {}},
                {
                    group: {
                        horizontal: True,
                        "items": [
                            {
                                input_text: {
                                    label: "Player Name",
                                    tag: "name_input",
                                    default_value: "Alice",
                                    callback: {
                                        put: [
                                            "player_name",
                                            lambda: j_to_dpg.controller.get_value(
                                                "name_input"
                                            ),
                                        ]
                                    },
                                }
                            },
                            {
                                checkbox: {
                                    label: "Sync",
                                    tag: "name_sync_check",
                                    default_value: True,
                                    callback: {
                                        "toggle_monitor": [
                                            "name_sync_check",
                                            "player_name",
                                            "name_display",
                                        ]
                                    },
                                }
                            },
                        ],
                    }
                },
                {
                    group: {
                        horizontal: True,
                        "items": [
                            {
                                slider_int: {
                                    label: "Player Level",
                                    tag: "level_input",
                                    default_value: 50,
                                    max_value: 100,
                                    callback: {
                                        put: [
                                            "player_level",
                                            lambda: j_to_dpg.controller.get_value(
                                                "level_input"
                                            ),
                                        ]
                                    },
                                }
                            },
                            {
                                checkbox: {
                                    label: "Sync",
                                    tag: "level_sync_check",
                                    default_value: True,
                                    callback: {
                                        "toggle_monitor": [
                                            "level_sync_check",
                                            "player_level",
                                            "level_display",
                                        ]
                                    },
                                }
                            },
                        ],
                    }
                },
                {
                    group: {
                        horizontal: True,
                        "items": [
                            {
                                checkbox: {
                                    label: "Premium Account",
                                    tag: "premium_input",
                                    default_value: True,
                                    callback: {
                                        put: [
                                            "is_premium",
                                            lambda: j_to_dpg.controller.get_value(
                                                "premium_input"
                                            ),
                                        ]
                                    },
                                }
                            },
                            {
                                checkbox: {
                                    label: "Sync",
                                    tag: "premium_sync_check",
                                    default_value: True,
                                    callback: {
                                        "toggle_monitor": [
                                            "premium_sync_check", 
                                            "is_premium",
                                            "premium_display",
                                        ]
                                    },
                                }
                            },
                        ],
                    }
                },
                {
                    group: {
                        horizontal: True,
                        "items": [
                            {
                                color_edit: {
                                    label: "Profile Color",
                                    tag: "color_input",
                                    default_value: [120, 150, 255, 255],
                                    no_alpha: True,
                                    callback: {
                                        put: [
                                            "profile_color",
                                            lambda: j_to_dpg.controller.get_value(
                                                "color_input"
                                            ),
                                        ]
                                    },
                                }
                            },
                            {
                                checkbox: {
                                    label: "Sync",
                                    tag: "color_sync_check",
                                    default_value: True,
                                    callback: {
                                        "toggle_monitor": [
                                            "color_sync_check",
                                            "profile_color",
                                            "color_display",
                                        ]
                                    },
                                }
                            },
                        ],
                    }
                },
                {
                    group: {
                        horizontal: True,
                        "items": [
                            {
                                drag_float: {
                                    label: "XP Boost",
                                    tag: "boost_input",
                                    default_value: 1.5,
                                    speed: 0.01,
                                    max_value: 5.0,
                                    format: "%.2f",
                                    callback: {
                                        put: [
                                            "xp_boost",
                                            lambda: j_to_dpg.controller.get_value(
                                                "boost_input"
                                            ),
                                        ]
                                    },
                                }
                            },
                            {
                                checkbox: {
                                    label: "Sync",
                                    tag: "boost_sync_check",
                                    default_value: True,
                                    callback: {
                                        "toggle_monitor": [
                                            "boost_sync_check",
                                            "xp_boost",
                                            "boost_display",
                                        ]
                                    },
                                }
                            },
                        ],
                    }
                },
            ],
        }
    },
    "display_window": {
        window: {
            label: "Display Window (Reactive)",
            width: 450,
            height: 350,
            pos: [470, 10],
            "display_window_inner": [
                {
                    text: {
                        default_value: "This window's values update if 'Sync' is enabled."
                    }
                },
                {separator: {}},
                {
                    group: {
                        horizontal: True,
                        "items": [
                            {text: {default_value: "Player Name:"}},
                            {text: {tag: "name_display"}},
                        ],
                    }
                },
                {
                    group: {
                        horizontal: True,
                        "items": [
                            {text: {default_value: "Player Level:"}},
                            {text: {tag: "level_display"}},
                        ],
                    }
                },
                {
                    group: {
                        horizontal: True,
                        "items": [
                            {text: {default_value: "Premium Status:"}},
                            {text: {tag: "premium_display"}},
                        ],
                    }
                },
                {
                    group: {
                        horizontal: True,
                        "items": [
                            {text: {default_value: "XP Boost:"}},
                            {text: {tag: "boost_display"}},
                        ],
                    }
                },
                {
                    group: {
                        horizontal: True,
                        "items": [
                            {text: {default_value: "Profile Color:"}},
                            {color_button: {tag: "color_display", no_inputs: True}},
                        ],
                    }
                },
            ],
        }
    },
    "state_display_window": {
        window: {
            label: "Internal State Monitor",
            width: 450,
            height: 340,
            pos: [470, 370],
            "display_window_controls": [
                {
                    group: {
                        horizontal: True,
                        horizontal_spacing: 20,
                        "displays": [
                            {
                                text: {
                                    tag: "store_display",
                                    default_value: "Loading Store...",
                                }
                            },
                            {
                                text: {
                                    tag: "monitors_display",
                                    default_value: "Loading Monitors...",
                                }
                            },
                        ],
                    }
                }
            ],
        }
    },
}

j_to_dpg.start(main_ui)