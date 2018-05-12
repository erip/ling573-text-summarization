from src.summarization.information_ordering.expert import Expert

class ExampleExpert(Expert):
    def __init__(self):
        self._name = "example"

    def order(self, d1, d2, partial_summary):
        """This expert will always place d1 ahead of d2"""
        return 0.51