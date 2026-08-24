from avl_index import AVLIndex


def test_insert_lookup_update_and_order():
    index = AVLIndex()
    for key in [40, 10, 70, 20, 60, 80, 30, 50]:
        index.set(key, f"v{key}")

    assert len(index) == 8
    assert index.get(60) == "v60"
    assert index.get(999) is None

    index.set(60, "changed")
    assert len(index) == 8
    assert index.get(60) == "changed"
    assert [k for k, _ in index.items()] == sorted([40, 10, 70, 20, 60, 80, 30, 50])

    ok, message = index.validate()
    assert ok, message


def test_delete_leaf_and_missing_key():
    index = AVLIndex()
    for key in [20, 10, 30, 5, 15]:
        index.set(key, key)

    assert index.delete(5) is True
    assert index.delete(999) is False
    assert len(index) == 4
    assert index.get(5) is None

    ok, message = index.validate()
    assert ok, message


def test_range_query_is_inclusive_and_sorted():
    index = AVLIndex()
    for key in range(0, 100, 5):
        index.set(key, key * 10)

    assert index.range_items(20, 40) == [
        (20, 200),
        (25, 250),
        (30, 300),
        (35, 350),
        (40, 400),
    ]
    assert index.range_items(10, 9) == []


def test_delete_simple_two_child_case():
    index = AVLIndex()
    for key in [20, 10, 30]:
        index.set(key, key)

    assert index.delete(20) is True
    assert [k for k, _ in index.items()] == [10, 30]
    ok, message = index.validate()
    assert ok, message
