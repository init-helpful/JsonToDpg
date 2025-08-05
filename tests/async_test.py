from testsetup import setup_pathing

setup_pathing()

import random
from jsontodpg import JsonToDpg


# --- Define Plugin Class ---
# The plugin's logic remains the same.
class TestPlugin:
    def __init__(self):
        self.controller = None
        self.stop_updates = True
        self.monitor_active = False

    def start_async_updates(self, slider_tag, text_tag, display_tag):
        if not self.controller or not self.stop_updates:
            return
        print("Starting async updates...")
        self.stop_updates = False

        def update_slider():
            if self.controller.component_exists(slider_tag):
                self.controller.set_value(slider_tag, random.randint(0, 100))

        def update_text():
            adjectives = ["amazing", "declarative", "simple", "powerful", "fun"]
            if self.controller.component_exists(text_tag):
                self.controller.set_value(
                    text_tag, f"JsonToDpg is {random.choice(adjectives)}!"
                )

        self.controller.add_async_function(
            interval=15,
            function=update_slider,
            end_condition=lambda: self.stop_updates,
            name="Slider Updater",
        )
        self.controller.add_async_function(
            interval=30,
            function=update_text,
            end_condition=lambda: self.stop_updates,
            name="Text Updater",
        )

        if not self.monitor_active:
            self.monitor_active = True
            self.controller.add_async_function(
                interval=30,
                function=lambda: self.monitor_async_stack(display_tag),
                end_condition=lambda: not self.monitor_active,
                name="Stack Monitor",
            )

    def stop_async_updates(self):
        print("Stopping async updates...")
        self.stop_updates = True

    def modify_task_interval(self, interval_tag, index_tag, new_interval_tag):
        if not self.controller:
            return
        try:
            old_interval = self.controller.get_value(interval_tag)
            task_index = self.controller.get_value(index_tag)
            new_interval = self.controller.get_value(new_interval_tag)
        except Exception as e:
            print(f"Error getting values from UI: {e}")
            return

        if new_interval <= 0:
            print("Error: New interval must be a positive number.")
            return
        if old_interval == new_interval:
            return

        async_dict = self.controller.jsontodpg.async_functions
        if old_interval not in async_dict or not (
            0 <= task_index < len(async_dict[old_interval])
        ):
            print(
                f"Error: Task at interval {old_interval}, index {task_index} not found."
            )
            return

        task_to_move = async_dict[old_interval].pop(task_index)
        task_to_move.interval = new_interval
        if new_interval not in async_dict:
            async_dict[new_interval] = []
        async_dict[new_interval].append(task_to_move)
        print(
            f"Success! Moved task '{task_to_move.name}' from interval {old_interval} to {new_interval}."
        )

    def monitor_async_stack(self, display_tag):
        if not self.controller or not self.controller.component_exists(display_tag):
            return
        async_dict = self.controller.jsontodpg.async_functions
        display_lines = ["--- Live Async Function Stack ---"]
        for interval in sorted(async_dict.keys()):
            functions = async_dict[interval]
            if not functions:
                continue
            display_lines.append(f"\nInterval {interval}:")
            for i, func_obj in enumerate(functions):
                status = (
                    "stopping"
                    if func_obj.end_condition()
                    else "paused" if func_obj.pause_condition() else "running"
                )
                display_lines.append(f"  - Task Index {i}: {func_obj.name} ({status})")
        self.controller.set_value(display_tag, "\n".join(display_lines))


# --- NEW WORKFLOW ---
# 1. Initialize JsonToDpg with the plugin.
jtd = JsonToDpg(plugins=[TestPlugin], debug=False)

# 2. Create a convenience alias for the keyword accessor.
k = jtd.keywords

# 3. Define the UI using the keyword accessor for everything.
main_ui = {
    k.viewport: {
        k.width: 800,
        k.height: 700,
        k.title: "Interactive Async Control Example",
    },
    k.window: {
        k.label: "Async Control Window",
        k.width: 780,
        k.height: 680,
        "ui_elements": [
            {
                k.slider_int: {
                    k.label: "Random Slider",
                    k.tag: "random_slider",
                    k.width: 400,
                }
            },
            {
                k.input_text: {
                    k.label: "Random Text",
                    k.tag: "random_text",
                    k.default_value: "Waiting for updates...",
                    k.readonly: True,
                    k.width: 400,
                }
            },
            {k.separator: {}},
        ],
        "control_buttons": {
            k.group: {
                k.horizontal: True,
                "buttons": [
                    {
                        k.button: {
                            k.label: "Start Async Updates",
                            k.callback: {
                                k.start_async_updates: [
                                    "random_slider",
                                    "random_text",
                                    "async_stack_display",
                                ]
                            },
                        }
                    },
                    {
                        k.button: {
                            k.label: "Stop Async Updates",
                            k.callback: {k.stop_async_updates: []},
                        }
                    },
                ],
            }
        },
        "modification_controls": [
            {k.separator: {}},
            {k.text: {k.default_value: "Modify Task Interval"}},
            {
                k.input_int: {
                    k.label: "Current Interval",
                    k.tag: "interval_input",
                    k.width: 300,
                }
            },
            {k.input_int: {k.label: "Task Index", k.tag: "index_input", k.width: 300}},
            {
                k.input_int: {
                    k.label: "New Interval",
                    k.tag: "new_interval_input",
                    k.width: 300,
                    k.default_value: 60,
                }
            },
            {
                k.button: {
                    k.label: "Modify Interval",
                    k.callback: {
                        k.modify_task_interval: [
                            "interval_input",
                            "index_input",
                            "new_interval_input",
                        ]
                    },
                }
            },
        ],
        "monitor_display": [
            {k.separator: {}},
            {k.text: {k.default_value: "Async Stack Display"}},
            {
                k.text: {
                    k.tag: "async_stack_display",
                    k.default_value: "Press 'Start' to begin monitoring.",
                }
            },
        ],
    },
}

# 4. Start the application.
jtd.start(main_ui)
