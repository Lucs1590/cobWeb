import Climas


def test_month_transformation():
    month = Climas.month_transform('março')
    assert month == 3
