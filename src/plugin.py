
SHARED_PYTHON_KEYWORDS = ["format"]
DEFAULT_ALTERING_KEYWORD_FILTERS = ["add_", "create_"]
DEFAULT_NON_ALTERING_KEYWORD_FILTERS = ["draw", "load_"]
KEYWORD_IGNORE_SUBSTRINGS = ["__"]

class plugin:
    def __init__(self):
        altering_keyword_filters = []
        non_altering_keyword__filters = []
        