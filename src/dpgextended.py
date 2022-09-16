from email.mime import image
import dearpygui.dearpygui as dpg


def __find_item_by_type(item_type):
    for _id in dpg.get_all_items():
        if item_type in dpg.get_item_type(_id):
            return _id


def find_texture_registry():
    texture_registry = __find_item_by_type("mvTextureRegistry")

    if not texture_registry:
        texture_registry = dpg.add_texture_registry()

    return texture_registry


def update_image(data, image_tag, texture_tag):
    pass


def __non_empty(dictionary):
    return {k: v for k, v in dictionary.items() if v}


def __image(
    texture_tag,
    image_tag,
    width,
    height,
    data,
    image_parent="",
    texture_function=dpg.add_raw_texture,
):

    if dpg.get_value(image_tag):
        if not image_parent:
            image_parent = dpg.get_item_parent(image_tag)
        dpg.delete_item(texture_tag)

    elif not image_parent:
        image_parent = dpg.last_container()

    if dpg.get_value(texture_tag):
        dpg.delete_item(texture_tag)

    dpg.add_image(
        **__non_empty(
            {
                "parent": image_parent,
                "tag": image_tag,
                "texture_tag": texture_function(
                    **__non_empty(
                        {
                            "width": width,
                            "height": height,
                            "default_value": data,
                            "parent": find_texture_registry(),
                        }
                    )
                ),
            }
        )
    )


def update_image(texture_tag, image_tag, image_parent, width, height, data, texture_function=dpg.add_raw_texture):
    __image(
        width=width,
        height=height,
        data=data,
        image_parent=image_parent,
        image_tag=image_tag,
        texture_tag=texture_tag,
    )



def image_from_file(
    image_tag, texture_tag, file_path="", texture_function=dpg.add_raw_texture
):

    width, height, channels, data = dpg.load_image(file_path)

    __image(
        width=width,
        height=height,
        data=data,
        image_tag=image_tag,
        texture_tag=texture_tag,
        texture_function=texture_function
    )
