# import dearpygui.dearpygui as dpg
from collections import OrderedDict
from utils import *

DEFAULT_ALTERING_KEYWORD_FILTERS = ["add_", "create_"]
DEFAULT_NON_ALTERING_KEYWORD_FILTERS = ["draw", "load_"]
KEYWORD_IGNORE_SUBSTRINGS = ["__", "dpg"]

class Tokenizer:
    def __init__(
        self,
        dpg,
        generate_keyword_file_name="", #dpgkeywords
        plugins = []
    ):
        
        self.component_parameter_relations = OrderedDict()
        self.components = {}
        self.parameters = []
        self.plugins = {}

        self.build_keyword_library(dpg)
        self.add_plugins(plugins)
            
        if generate_keyword_file_name:
            self.write_to_file(generate_keyword_file_name)

    def __filter_keyword(
        self, function_name, altering_filters=[], non_altering_filters=[]
    ):
        """
            Not all dearpygui functions make sense in json format.
            This checks against the desired substrings.
            e.g. functions starting with substring 'create_'.

        Args:
            filtered_keyword (str, optional):
        """
        if not altering_filters and not non_altering_filters:
            if not [sub for sub in KEYWORD_IGNORE_SUBSTRINGS if (sub in function_name)]:
                if not function_name == function_name.upper():
                    return function_name

        if altering_filters:
            filtered_keyword = check_for_substrings(
                function_name, altering_filters, return_difference=True
            )
            if filtered_keyword:
                return filtered_keyword

        if non_altering_filters:
            filtered_keyword = check_for_substrings(function_name, non_altering_filters)
            if filtered_keyword:
                return filtered_keyword

    def build_keyword_library(
        self,
        package,
        altering_filters=DEFAULT_ALTERING_KEYWORD_FILTERS,
        non_altering_filters=DEFAULT_NON_ALTERING_KEYWORD_FILTERS,
    ):
        for function_name in dir(package):
            filtered_keyword = self.__filter_keyword(
                function_name, altering_filters, non_altering_filters
            )
            if filtered_keyword:
                filtered_keyword = clean_keyword(filtered_keyword)
                function_reference = getattr(package, function_name)
                self.components[filtered_keyword] = function_reference

                params = clean_keywords_list(
                    [
                        param
                        for param in function_reference.__code__.co_varnames
                        if not param in ["args", "kwargs"]
                    ]
                )

                # Add non-existing parameters to master parameter list
                self.parameters = self.parameters + [
                    param for param in params if not param in self.parameters
                ]

                self.component_parameter_relations[filtered_keyword] = params
        


    def add_plugins(self, plugins):
        for plugin in plugins:
            if callable(plugin):
            
                instance = plugin()
                self.plugins[plugin.__name__] = instance
                for func_name in dir(instance):
                    if callable(getattr(instance, func_name)) and not func_name.startswith('_'):
                        func_ref = getattr(instance, func_name)
                        full_func_name = f'{plugin.__name__.lower()}_{func_name.lower()}'
                        self.components[full_func_name] = func_ref
                        
                        # Add parameters for the function
                        params = [param for param in func_ref.__code__.co_varnames if param != 'self']
                        self.parameters.extend(params)
                        
                        # Update component_parameter_relations
                        self.component_parameter_relations[full_func_name] = params
            else:
                self.build_keyword_library(plugin)


    def write_to_file(self, file_name):
        string = "#THIS FILE WAS GENERATED\n"
        components = list(self.components.keys())

        string = (
            string + f"#--------------COMPONENTS--------------[{len(components)}]\n"
        )

        for component in components:
            string = string + "\n" + f'{component}="{component}"'

        string = (
            string
            + "\n"
            + f"\n#--------------PARAMETERS--------------[{len(self.parameters)}]\n"
        )

        for param in self.parameters:
            string = string + "\n" + f'{param}="{param}"'

        string = (
            string
            + "\n\n"
            + f"component_parameter_relations = {remove_quotes(str(dict(self.component_parameter_relations)))}"
        )
        string = string + "\n" + f"__all__ = {components + self.parameters}"

        write_to_py_file(file_name=file_name, data=string)
