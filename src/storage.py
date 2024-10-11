import polars as pl

class Storage:
    def __init__(self):
        self.storage = {'flat': {}, 'nested': {}}

    def put(self, key_path, value):
        """
        Stores a value at the specified key path.
        
        Args:
            key_path (str): A string representing the path to store the value, separated by periods.
            value (Any): The value to store.
        """
        keys = self._split_key_path(key_path)
        if len(keys) == 1:
            # Flat storage
            self.storage['flat'][keys[0]] = value
        else:
            # Nested storage
            current_dict = self.storage['nested']
            for i, key in enumerate(keys[:-1]):
                if key not in current_dict:
                    current_dict[key] = {}
                current_dict = current_dict[key]
            
            # Set the final value
            current_dict[keys[-1]] = value

    def get(self, key_path):
        """
        Retrieves the value associated with the given key path.
        
        Args:
            key_path (str): A string representing the path to retrieve the value, separated by periods.
        
        Returns:
            Any: The value associated with the key path, or None if not found.
        """
        keys = self._split_key_path(key_path)
        if len(keys) == 1:
            # Flat storage lookup
            return self.storage['flat'].get(keys[0])
        else:
            # Nested storage lookup
            current_dict = self.storage['nested']
            for key in keys[:-1]:
                if isinstance(current_dict, dict) and key in current_dict:
                    current_dict = current_dict[key]
                else:
                    break
            
            # Check the final key
            if isinstance(current_dict, dict) and keys[-1] in current_dict:
                return current_dict[keys[-1]]
        
        return None

    def _split_key_path(self, key_path):
        """
        Splits a string key path into a list of keys.
        
        Args:
            key_path (str): A string representing the path, separated by periods.
        
        Returns:
            list: A list of keys.
        """
        return [key for key in key_path.split('.') if key]

    def contains(self, key_path):
        """
        Checks if a key path exists in the storage.
        
        Args:
            key_path (str): A string representing the path to check.
        
        Returns:
            bool: True if the key path exists, False otherwise.
        """
        keys = self._split_key_path(key_path)
        if len(keys) == 1:
            return key_path in self.storage['flat']
        else:
            current_dict = self.storage['nested']
            for key in keys[:-1]:
                if isinstance(current_dict, dict) and key in current_dict:
                    current_dict = current_dict[key]
                else:
                    break
            
            # Check the final key
            return isinstance(current_dict, dict) and keys[-1] in current_dict

    def ref(self):
        """
        Returns a reference to the instance of storage.
        
        Returns:
            OptimizedStoragePolars: A reference to the current instance.
        """
        return self

# # Example usage
# storage = Storage()

# # Store some values
# storage.put('a', 'value_a')
# storage.put('b', 'value_b')
# storage.put('users.data.name', 'Alice')
# storage.put('users.data.age', 30)

# # Retrieve values
# result_a = storage.get('a')
# print(f"Value for 'a': {result_a}")  # Should print 'value_a'

# name = storage.get('users.data.name')
# age = storage.get('users.data.age')
# print(f"Nested value for 'users.data.name': {name}")  # Should print 'Alice'
# print(f"Nested value for 'users.data.age': {age}")  # Should print 30

# # Get instance reference
# instance_ref = storage.get_instance()
# print(f"Instance reference: {instance_ref}")  # Should print the instance of OptimizedStoragePolars

# # Use the instance reference to perform operations
# result_b = instance_ref.get('b')
# print(f"Value for 'b' using instance reference: {result_b}")  # Should print 'value_b'
