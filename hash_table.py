# hash_table.py

from typing import NamedTuple, Any


DELETED = object()  # sentinel value for linear probing


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
        # self._slots[self._index(key)] = Pair(key, value)
        for index, pair in self._probe(key):
            if pair is DELETED: continue  # collsion has occurred before
            if pair is None or pair.key == key:  # new key or update
                self._slots[index] = Pair(key, value)
                break
        else:
            raise MemoryError("Not enough capacity")  # exhausted all avail slots


    def __getitem__(self, key):
        # pair: Pair = self._slots[self._index(key)]
        # if pair is None:
        #     raise KeyError(key)
        # return pair.value
        for _, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                return pair.value
        raise KeyError(key)
    

    def __delitem__(self, key):
        # if key in self:
        #     self._slots[self._index(key)] = None
        # else:
        #     raise KeyError(key)
        for index, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                self._slots[index] = DELETED
                return
        raise KeyError(key)
    

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True
        
    
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
    

    def __eq__(self, other):
        if self is other:  # same id()
            return True
        if type(self) is not type(other):
            return False
        return set(self.pairs) == set(other.pairs)
    

    def _index(self, key) -> int:
        return hash(key) % self.capacity


    def _probe(self, key):
        index = self._index(key)
        for _ in range(self.capacity):
            yield index, self._slots[index]
            index = (index + 1) % self.capacity  # modulo wraps index around origin if necessary


    def get(self, key, default = None):
        try:
            return self[key]
        except KeyError:
            return default
    

    def copy(self):
        return HashTable.from_dict(dict(self.pairs), self.capacity)
    

    def clear(self):
        self._slots = self.capacity * [None]
    

    @property
    def pairs(self):
        return {
            pair for pair in self._slots
            if pair not in (None, DELETED)
        }
    

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
    # ----------------------------------------------------------
    # ad hoc testing
    # ----------------------------------------------------------
    # from os import environ

    # environ["PYTHONHASHSEED"] = "0"
    # source = {'hello': 'world', 1: 2, True: False}
    # ht = HashTable.from_dict(source, capacity=len(source))
    # print(ht)
    from unittest.mock import patch

    with patch('builtins.hash', return_value=24):
        ht = HashTable(capacity=100)
        # Test collision handling on create
        ht['easy'] = 'Requires little effort'
        ht['medium'] = 'Requires some skill and effort'
        ht['difficult'] = 'Needs much skill'
    
        print(ht._slots[24])
        print(ht._slots[25])
        print(ht._slots[26])

        # Test collision handling on delete
        del ht['medium']

        print(ht._slots[24])
        print(ht._slots[25])
        print(ht._slots[26])