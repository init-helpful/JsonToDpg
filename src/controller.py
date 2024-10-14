from store import Store

class Controller:
    def __init__(self, jsontodpg):
        self.jsontodpg = jsontodpg
        self.store = Store()

    def hide(self, tag):
        self.jsontodpg.dpg.hide_item(tag)

    def show(self, tag):
        self.jsontodpg.dpg.show_item(tag)
    
    def component_exists(self, tag):
        return self.jsontodpg.dpg.does_item_exist(tag)
    
    def get_label_text(self,tag):
        return self.jsontodpg.dpg.get_item_label(tag)

    def get_value(self, tag):
        return self.jsontodpg.dpg.get_value(tag)

    def set_value(self, tag, value):
        self.jsontodpg.dpg.set_value(tag,value)
        
    def get_state(self, tag):
        return self.jsontodpg.dpg.get_item_state(tag)

    def delete_element(self, tag):
        self.jsontodpg.dpg.delete_item(tag)
        
    def delete_all(self, tags=[]):
        for tag in tags:
            self.delete(tag)

    def spawn(self, json_data, check_for_existing=False):
        self.jsontodpg.parse(json_data, check_for_existing)


    # Model Functions --------------------------------

    def store_contains(self, key_path):
        return self.store.contains(key_path)

    def put(self,key_path, value):
        self.store.put(key_path,value)
    
    def get(self,key_path):
        return self.store.get(key_path)
        
    # Utils --------------------------------

    def list_to_sublists(self, main_list, sub_list_size=4):
        return [
            main_list[x : x + sub_list_size]
            for x in range(0, len(main_list), sub_list_size)
        ]

    def add_async_function(
        self, interval, function, end_condition=None, pause_condition=None, num_cycles=0
    ):
        self.jsontodpg.add_async_function(
            interval, function, end_condition, pause_condition, num_cycles
        )