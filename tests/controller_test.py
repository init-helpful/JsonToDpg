from testsetup import setup_pathing

setup_pathing()

import time as systime
from jsontodpg import JsonToDpg


from dpgkeywords import *


class ControllerTestPlugin:
    """
    A dedicated plugin to house the callback functions for testing the controller.
    This demonstrates how controller methods can be leveraged from within the app's logic.
    """

    def __init__(self):
        self.controller = None
        self.spawn_counter = 0

    def test_spawn_simple(self, parent_tag, results_tag):
        """Spawns a simple, single UI element into a specified parent."""
        if not self.controller:
            return

        self.spawn_counter += 1
        spawned_tag = f"spawned_button_{self.spawn_counter}"
        spawned_label = f"Spawned Button #{self.spawn_counter}"

        # Define the UI element to be created dynamically
        spawn_json = {button: {label: spawned_label, tag: spawned_tag}}

        # Use the controller to spawn the element
        self.controller.spawn(spawn_json, parent=parent_tag)

        # Verify the result and update the display
        systime.sleep(0.01)  # <--- FIX: Use the renamed module
        if self.controller.component_exists(spawned_tag):
            result_text = f"SUCCESS: Spawned '{spawned_tag}' into '{parent_tag}'."
        else:
            result_text = f"FAILURE: Could not find '{spawned_tag}' after spawn call."
        self.controller.set_value(results_tag, result_text)

    def test_spawn_nested(self, parent_tag, results_tag):
        """Spawns a complex, nested UI structure into a specified parent."""
        if not self.controller:
            return

        self.spawn_counter += 1
        header_tag = f"spawned_header_{self.spawn_counter}"

        # Define a more complex, nested structure
        spawn_json = {
            collapsing_header: {
                label: "Spawned Nested Elements",
                tag: header_tag,
                "content": [
                    {text: {default_value: "This text is inside the spawned header."}},
                    {
                        group: {
                            horizontal: True,
                            "items": [
                                {checkbox: {label: "Spawned Checkbox"}},
                                {button: {label: "Another Spawned Button"}},
                            ],
                        }
                    },
                ],
            }
        }

        # Use the controller to spawn the entire structure
        self.controller.spawn(spawn_json, parent=parent_tag)

        # Verify and report
        systime.sleep(0.01)
        if self.controller.component_exists(header_tag):
            result_text = (
                f"SUCCESS: Spawned nested structure with root '{header_tag}' "
                f"into '{parent_tag}'."
            )
        else:
            result_text = (
                f"FAILURE: Could not find root of nested spawn '{header_tag}'."
            )
        self.controller.set_value(results_tag, result_text)

    def run_all_tests(self, subject_tag, deletable_tag, results_tag):
        """Runs a battery of tests against various controller functions."""
        if not self.controller:
            return

        results = ["--- Controller Function Test Results ---"]

        # 1. Test: store_contains / put / get
        self.controller.put("test_key", "initial_value")
        results.append(f"put: Stored 'initial_value' at 'test_key'")
        results.append(
            f"store_contains: Key 'test_key' exists -> {self.controller.store_contains('test_key')}"
        )
        results.append(f"get: Retrieved '{self.controller.get('test_key')}'")
        self.controller.put("test_key", "updated_value")
        results.append(f"get (after update): Retrieved '{self.controller.get('test_key')}'")
        results.append("-" * 20)

        # 2. Test: get_value
        initial_val = self.controller.get_value(subject_tag)
        results.append(f"get_value: Initial value is '{initial_val}'")

        # 3. Test: set_value
        self.controller.set_value(subject_tag, "Value Set by Controller!")
        results.append(f"set_value: Set value to 'Value Set by Controller!'")
        new_val = self.controller.get_value(subject_tag)
        results.append(f"get_value (after set): New value is '{new_val}'")
        results.append("-" * 20)
        
        # 4. Test: get_label_text
        label = self.controller.get_label_text(subject_tag)
        results.append(f"get_label_text: Label is '{label}'")
        results.append("-" * 20)

        # 5. Test: hide/show and get_state
        self.controller.hide(subject_tag)
        state_after_hide = self.controller.get_state(subject_tag)
        results.append(f"hide: Item hidden. Visible state: {state_after_hide['visible']}")
        self.controller.show(subject_tag)
        state_after_show = self.controller.get_state(subject_tag)
        results.append(f"show: Item shown. Visible state: {state_after_show['visible']}")
        results.append("-" * 20)
        
        # 6. Test: delete_element and component_exists
        results.append(f"component_exists (before): '{deletable_tag}' exists -> {self.controller.component_exists(deletable_tag)}")
        self.controller.delete_element(deletable_tag)
        results.append(f"delete_element: Called on '{deletable_tag}'")
        results.append(f"component_exists (after): '{deletable_tag}' exists -> {self.controller.component_exists(deletable_tag)}")
        results.append("-" * 20)

        # 7. Test: list_to_sublists
        sublists = self.controller.list_to_sublists(list(range(9)), 4)
        results.append(f"list_to_sublists([0-8], 4): -> {sublists}")

        # Final Update
        self.controller.set_value(results_tag, "\n".join(results))


# --- Step 1: Initialize the library with our test plugin ---
jtd = JsonToDpg(plugins=[ControllerTestPlugin], debug=False)

# --- Step 2: Define the UI using keywords for everything ---
main_ui = {
    viewport: {
        width: 1000,
        height: 700,
        title: "Controller Function Test",
    },
    window: {
        label: "Controller Test Window",
        width: -1, # Fill width
        height: -1, # Fill height
        "main_layout": [
            {text: {default_value: "This window tests the core controller methods."}},
            {
                group: {
                    horizontal: True,
                    "buttons": [
                        {
                            button: {
                                label: "Spawn Simple Button in Target 1",
                                callback: {
                                    "test_spawn_simple": [
                                        "spawn_target_1",
                                        "test_results_text",
                                    ]
                                },
                            }
                        },
                        {
                            button: {
                                label: "Spawn Nested Structure in Target 2",
                                callback: {
                                    "test_spawn_nested": [
                                        "spawn_target_2",
                                        "test_results_text",
                                    ]
                                },
                            }
                        },
                    ],
                }
            },
            {separator: {}},
            {text: {default_value: "Spawn Targets:"}},
            {child_window: {width: -1, height: 150, "content": [
                {group: {tag: "spawn_target_1", label: "Target 1"}},
                {group: {tag: "spawn_target_2", label: "Target 2"}},
            ]}},
            {separator: {}},
            {
                text: {
                    default_value: "Generic Controller Function Tests:"
                }
            },
            {
                group: {
                    horizontal: True,
                    "items": [
                        {
                            input_text: {
                                label: "Test Subject",
                                tag: "test_subject_input",
                                default_value: "Initial Value",
                            }
                        },
                        {
                            text: {
                                tag: "deletable_text_item",
                                default_value: "-> I will be deleted by the test.",
                            }
                        },
                    ],
                }
            },
            {
                button: {
                    label: "Run All Controller Function Tests",
                    callback: {
                        "run_all_tests": [
                            "test_subject_input",
                            "deletable_text_item",
                            "test_results_text",
                        ]
                    },
                }
            },
            {separator: {}},
            {
                child_window: {
                    label: "Test Results",
                    width: -1,
                    height: 250,
                    "content": [
                        {
                            text: {
                                tag: "test_results_text",
                                default_value: "Click a button to see test results here.",
                            }
                        }
                    ],
                }
            },
        ],
    },
}

# --- Step 3: Start the application ---
jtd.start(main_ui)