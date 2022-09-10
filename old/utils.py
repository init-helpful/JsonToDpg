from consts import *




def pl(l):
    [print(i) for i in l]

def remove_non_matching(dictionary, filter_list):
    filtered = {}
    for item in dictionary.keys():
        if item in filter_list:
            filtered[item] = dictionary[item]
    return filtered


def list_difference(list_one, list_two):
    if list_one and list_two:
        if len(list_one) > len(list_two):
            return list_two
        for i in range(len(list_one)):
            if list_one[i] != list_two[i]:
                return list_two[i:]


def find_parent_path(current_path, level, path_list):

    for path in path_list[::-1]:
        split_path = path.split(KEY_SPLIT_CHAR)
        if current_path[0] == split_path[0]:
            if len(split_path) <= level:
                return split_path
        else:
            return None


def check_for_substrings(string, comparison_list):
    for sub in comparison_list:
        if sub in string:
            return sub


def build_function_lookup():
    items = {}
    for function_name in dir(dpg):
        found_substring = check_for_substrings(
            function_name, function_substring_filters
        )
        if found_substring:

            items[function_name.replace(found_substring, "")] = getattr(
                dpg, function_name
            )
        elif function_name in other_functions:
            items[function_name] = getattr(dpg, function_name)

    return items


def count_numeric_values(lst):
    count = 0
    for item in lst:
        if item.isnumeric():
            count += 1
    return count





def flatten(dictionary,key_split_char=KEY_SPLIT_CHAR):
    """
    Function that converts stanadard dictionaries to a flattened state for string comparison
    and mapping of dictionaries.

    Example at top of class.

    Indexed Keyless Dict Example:
        "Example": [
            {"This":"dictionary","Is":"Keyless"},
            {"So":"Is","This":"One"}
        ]

        Flattened looks like :

            {
                "Example->0->This":"dictionary",
                "Example->0->Is":"Keyless",
                "Example->1->So":"Is",
                "Example->1->This":"One"
            }
    """

    prop_paths = {}
    try:

        for key, val in dictionary.items():
            if isinstance(val, dict) and val:
                # If the item is a dictionary then recursively call flatten to go further down the path
                deeper = flatten(val).items()
                prop_paths.update(
                    {key + key_split_char + key2: val2 for key2, val2 in deeper}
                )
            elif isinstance(val, list):
                # If the item is a list then recursively call flatten for each item in the list
                for dict_index, list_of_keyless_dicts in enumerate(
                    val
                ):  # Apply indexing to non-keyed dictionaries
                    deeper = flatten({str(dict_index): list_of_keyless_dicts}).items()

                    prop_paths.update(
                        {key + key_split_char + key2: val2 for key2, val2 in deeper}
                    )
            else:
                # If the item is not a dict or list then it is a value we will assign to the key
                prop_paths[key] = val
        return prop_paths
    except AttributeError:
        print("Dictionary could not be flattend!")
        return prop_paths
