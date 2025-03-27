
class AsyncFunction:
    def __init__(
        self,
        interval,
        function_reference,
        end_condition,
        pause_condition,
        cycles=0,
    ):
        self.interval = interval
        self.function_reference = function_reference
        self.cycles = cycles
        self.times_performed = 0
        self.end_condition = end_condition if end_condition else lambda : False
        self.pause_condition = pause_condition if pause_condition else lambda : False

    def run(self):

        self.function_reference()
