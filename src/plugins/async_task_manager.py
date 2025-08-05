class AsyncTaskManager:
    """
    A reusable plugin that provides methods to monitor and manage
    the application's running asynchronous tasks.
    """

    def __init__(self):
        # This controller instance will be injected by JsonToDpg.
        self.controller = None

    def display_tasks(self, display_tag):
        """
        Inspects the main async function stack and updates a UI text element
        with a formatted, real-time display of all running tasks.

        This method is designed to be run repeatedly by an async task itself.
        """
        if not self.controller or not self.controller.component_exists(display_tag):
            return

        async_dict = self.controller.jsontodpg.async_functions
        display_lines = ["--- Live Async Task Stack ---"]

        if not any(async_dict.values()):
            display_lines.append("\n(No active async tasks)")
        else:
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
                    display_lines.append(
                        f"  - Task Index {i}: {func_obj.name} ({status})"
                    )

        formatted_string = "\n".join(display_lines)
        self.controller.set_value(display_tag, formatted_string)

    def modify_task_interval(self, interval_tag, index_tag, new_interval_tag):
        """
        Finds a task by its current interval and index (from UI inputs)
        and moves it to a new interval.
        """
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
            print("Info: Old and new intervals are the same. No action taken.")
            return

        async_dict = self.controller.jsontodpg.async_functions

        if old_interval not in async_dict or not (
            0 <= task_index < len(async_dict[old_interval])
        ):
            print(
                f"Error: Task at interval {old_interval}, index {task_index} not found."
            )
            return

        # Perform the move
        task_to_move = async_dict[old_interval].pop(task_index)
        task_to_move.interval = new_interval

        if new_interval not in async_dict:
            async_dict[new_interval] = []

        async_dict[new_interval].append(task_to_move)
        print(
            f"Success! Moved task '{task_to_move.name}' from interval {old_interval} to {new_interval}."
        )
