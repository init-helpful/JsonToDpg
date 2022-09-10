def children(obj):
    children_objects = []
    children_variables = []

    object_types = {
        "tuple": lambda obj: obj,
        "dict": lambda obj: obj.items(),
        "list": lambda obj: obj,
    }

    for x in object_types[type(obj).__name__](obj):
        if type(x).__name__ in object_types:
            children_objects.append(x)
        else:
            children_variables.append(x)

    return children_objects, children_variables

def build_tree(obj, level_num=0, variables=[], levels=[]):
    children_objects, children_variables = children(obj)

    if len(children_objects) > 0:
        for child in children_objects:
            build_tree(
                obj=child, level_num=level_num + 1, variables=variables, levels=levels
            )

    if children_variables:
        variables.insert(0, children_variables)
        levels.insert(0, level_num - 1)

    return variables[::-1], levels[::-1]









test = {
    "a": [1, 2, 3, 4],
    "b": ["1"],
    "c": ["1"],
    "d": ["1"],
    "e": ["1"],
    "f": ["1"],
    "g": {"one": ["1", "2"]},
}


print(build_tree(test))

