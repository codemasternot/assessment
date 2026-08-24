from hash_cache import HashCache


def test_put_get_update_and_capacity():
    cache = HashCache(max_items=3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)

    assert cache.get("a") == 1
    cache.put("a", 10)
    assert cache.get("a") == 10
    assert len(cache) == 3

    ok, message = cache.validate()
    assert ok, message


def test_lru_eviction_basic_case():
    cache = HashCache(max_items=2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1

    cache.put("c", 3)

    assert cache.contains("a")
    assert not cache.contains("b")
    assert cache.contains("c")


def test_delete_and_reinsert_non_colliding_keys():
    cache = HashCache(max_items=4)
    cache.put(1, "one")
    cache.put(2, "two")
    cache.put(3, "three")

    assert cache.delete(2) is True
    assert cache.delete(2) is False
    assert cache.get(1) == "one"
    assert cache.get(3) == "three"

    cache.put(4, "four")
    assert cache.get(4) == "four"

    ok, message = cache.validate()
    assert ok, message


def test_missing_key_default():
    cache = HashCache(max_items=2)
    cache.put("x", 1)
    assert cache.get("missing") is None
    assert cache.get("missing", 99) == 99
