from recordclass import make_dataclass
from typing import Any, Optional

# Create optimized storage item class
StorageItem = make_dataclass('StorageItem', 'key value')

class Model:
    __slots__ = ('storage',)  # Memory optimization
    
    def __init__(self):
        """Initialize an empty storage model using RecordClass."""
        self.storage: dict[str, StorageItem] = {}
    
    def put(self, key: str, value: Any) -> None:
        """
        Stores a value at the specified key path.
        
        Args:
            key (str): A string representing the path to store the value
            value (Any): The value to store (can be any Python object)
        """
        self.storage[key] = StorageItem(key, value)
    
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieves the value associated with the given key path.
        
        Args:
            key (str): A string representing the path to retrieve
            
        Returns:
            Optional[Any]: The value associated with the key path, or None if not found
        """
        item = self.storage.get(key)
        return item.value if item else None
    
    def contains(self, key: str) -> bool:
        """
        Checks if a key path exists in the storage.
        
        Args:
            key (str): A string representing the path to check
            
        Returns:
            bool: True if the key path exists, False otherwise
        """
        return key in self.storage
    
    def ref(self) -> 'OptimizedModel':
        """Returns a reference to the instance."""
        return self