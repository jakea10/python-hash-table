from hash_table import HashTable
import pytest


# def test_should_always_pass():
#     assert 2 + 2 == 4, "This is just a dummy test"


def test_should_create_hash_table():
    assert HashTable(capacity=100) is not None


def test_should_report_capacity():
    assert len(HashTable(capacity=100)) == 100


def test_should_create_empty_value_slots():
    assert HashTable(capacity=3)._pairs == [None, None, None]


def test_should_not_contain_none_value_when_created():
    hash_table = HashTable(capacity=10)
    values = [pair.value for pair in hash_table.pairs]
    assert None not in values


@pytest.fixture
def hash_table() -> HashTable:
    sample_data = HashTable(capacity=100)
    sample_data["hello"] = "world"
    sample_data[98.6] = 37
    sample_data[True] = False
    sample_data["key"] = None
    return sample_data


def test_should_insert_key_value_pairs(hash_table: HashTable):
    assert ("hello", "world") in hash_table.pairs
    assert (98.6, 37) in hash_table.pairs
    assert (True, False) in hash_table.pairs
    assert ("key", None) in hash_table.pairs

    # # bypass shrink/grow tests below
    # assert len(ht) == 10


def test_should_not_grow_when_adding_elements():
    ht = HashTable(capacity=10)
    ht["foo"] = "bar"

    assert len(ht) == 10


def test_should_find_value_by_key(hash_table):
    assert hash_table["hello"] == "world"
    assert hash_table[98.6] == 37
    assert hash_table[True] is False
    assert hash_table["key"] is None


def test_should_raise_error_on_missing_key():
    hash_table = HashTable(capacity=10)
    with pytest.raises(KeyError) as exception_info:
        hash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"


def test_should_find_key(hash_table):
    assert "hello" in hash_table


def test_should_not_find_key(hash_table):
    assert "missing_key" not in hash_table


def test_should_get_value(hash_table):
    assert hash_table.get("hello") == "world"


def test_should_get_none_when_missing_key(hash_table):
    assert hash_table.get("missing_key") is None


def test_should_get_default_value_when_missing_key(hash_table):
    assert hash_table.get("missing_key", "default") == "default"


def test_should_get_value_with_default(hash_table):
    assert hash_table.get("hello", "default") == "world"


def test_should_delete_key_value_pair(hash_table):
    assert "hello" in hash_table
    assert ("hello", "world") in hash_table.pairs

    del hash_table["hello"]

    assert "hello" not in hash_table
    assert ("hello", "world") not in hash_table.pairs


def test_should_not_shrink_when_removing_elements(hash_table):
    del hash_table["hello"]
    assert len(hash_table) == 100


def test_should_raise_key_error_when_deleting(hash_table):
    with pytest.raises(KeyError) as exception_info:
        del hash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"


def test_should_update_value(hash_table):
    assert hash_table["hello"] == "world"

    hash_table["hello"] = "there"

    assert hash_table["hello"] == "there"
    assert hash_table[98.6] == 37
    assert hash_table[True] is False
    assert hash_table["key"] is None
    assert len(hash_table) == 100


def test_should_return_pairs(hash_table):
    assert ("hello", "world") in hash_table.pairs
    assert (98.6, 37) in hash_table.pairs
    assert (True, False) in hash_table.pairs
    assert ("key", None) in hash_table.pairs


def test_should_return_copy_of_pairs(hash_table):
    # Test defensive copying
    assert hash_table.pairs is not hash_table.pairs


def test_should_not_include_blank_pairs(hash_table):
    assert None not in hash_table.pairs