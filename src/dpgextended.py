import dearpygui.dearpygui as dpg


STATIC = "static"
DYNAMIC = "dynamic"
RAW = "raw"


def __find_item_by_type(item_type):
    
    for _id in dpg.get_all_items():
        if item_type in dpg.get_item_type(_id):
            return _id


def __find_texture_registry():
    texture_registry = __find_item_by_type("mvTextureRegistry")
    
    if not texture_registry:
        texture_registry = dpg.add_texture_registry()
        
    return texture_registry


def __image_from_file(
    file_path="",
    tag="",
    parent="",
    texture_tag="",
    texture_function=dpg.add_raw_texture,
):
    
    image_parent = dpg.last_container()
    width, height, channels, data = dpg.load_image(file_path)
    texture_args = {
        "width": width,
        "height": height,
        "default_value": data,
        "parent": __find_texture_registry(),
    }

    if texture_tag:
        texture_args.update({"tag": texture_tag})

    texture_id = texture_function(**texture_args)

    image_args = {
        "parent": image_parent,
        "texture_tag": texture_id,
    }
    
    if texture_tag:
        image_args.update({"texture_tag": texture_tag})

    
    print(texture_args)
    
    if tag:
        image_args.update({"tag": tag})
    if parent:
        image_args.update({"parent": parent})

    dpg.add_image(**image_args)


def static_image(file_path, **args):
    __image_from_file(file_path, texture_function=dpg.add_static_texture, **args)


def dynamic_image(file_path, **args):
    __image_from_file(file_path, texture_function=dpg.add_dynamic_texture, **args)


def raw_image(file_path, **args):
    __image_from_file(file_path, texture_function=dpg.add_raw_texture, **args)
