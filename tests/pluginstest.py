from testsetup import setup_pathing
setup_pathing()


from dpgkeywords import *
from jsontodpg import JsonToDpg





class TestPlugin():
    
    def test_plugin_print(string):
        print("hit")
        print(dir(string))
        
        
j_to_dpg = JsonToDpg(generate_keyword_file_name="aaa", debug=False, plugins=[TestPlugin])
c = j_to_dpg.controller

c.put("default_width", 400)
c.put("default_height", 400)
    
    


def windows():
    return [
        {
            window: {
                # "gen_random_number": c.add_async_function(
                #     interval=20, function={"testplugin_test_plugin_print":"test"}
                # ),
                
                label: "Window 1",
                pos: [0, 0],
                width: c.get("default_width"),
                height: c.get("default_height"),
                button: {
                    "label": "Change Text",
                    tag: "BUTTON1",
                    callback: lambda: c.set_value(
                        tag="INPUT2", value=c.get_value("INPUT1")
                    ),
                },
                input_text: {default_value: "type here", tag: "INPUT1"},
                "test_plugin_print":"t",
            }
        },
        
    ]


main = {viewport: {width: 800, height: 400}, "windows": windows()}

j_to_dpg.start(main)