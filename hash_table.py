# hash_table.py

from typing import NamedTuple, Any


class Pair(NamedTuple):
    key: Any
    value: Any


class HashTable:
    def __init__(self, capacity: int):
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Capacity must be a positive integer")
        self._slots = capacity * [None]


    def __len__(self):
        return len(self.pairs)
    

    def __setitem__(self, key, value):
        self._slots[self._index(key)] = Pair(key, value)


    def __getitem__(self, key):
        pair: Pair = self._slots[self._index(key)]
        if pair is None:
            raise KeyError(key)
        return pair.value
    

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True
        

    def get(self, key, default = None):
        try:
            return self[key]
        except KeyError:
            return default
        

    def __delitem__(self, key):
        if key in self:
            self._slots[self._index(key)] = None
        else:
            raise KeyError(key)
        
    
    def __iter__(self):
        yield from self.keys
    

    def __str__(self):
        pairs = []
        for key, value in self.pairs:
            pairs.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(pairs) + "}"
    

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}.from_dict({str(self)})"
    

    def _index(self, key) -> int:
        return hash(key) % self.capacity
    

    @property
    def pairs(self):
        return {pair for pair in self._slots if pair}
    

    @property
    def values(self):
        return [pair.value for pair in self.pairs]
    

    @property
    def keys(self):
        return {pair.key for pair in self.pairs}
    

    @property
    def capacity(self):
        return len(self._slots)


    @classmethod
    def from_dict(cls, dictionary: dict, capacity: int = None):
        hash_table = cls(capacity or len(dictionary) * 10)
        for key, value in dictionary.items():
            hash_table[key] = value
        return hash_table
    

if __name__ == "__main__":
    # ad hoc testing
    hash_table = HashTable(capacity=100)
    hash_table["hello"] = "world"
    hash_table[98.6] = 37
    hash_table[True] = False
    hash_table["key"] = None

    for key, value in hash_table.pairs:
        print(f"key={key}, value={value}")