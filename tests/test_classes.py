from pipm.classes import OrderedDefaultDict


def test_ordered_default_dict_of_list():
    dt = OrderedDefaultDict(list)
    dt[1].append("one")
    dt[2].append("two")
    assert list(dt.items()) == [(1, ['one']), (2, ['two'])]
