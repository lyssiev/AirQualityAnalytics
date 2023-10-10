import pytest
import utils


def testing_sumvalues():
    assert utils.sumvalues([1, 2, 3, 4]) == 10


def testing_sumvalues_exception():
    with pytest.raises(Exception):
        assert utils.sumvalues([1, 2, 3, "a"])


def testing_maxvalue():
    assert utils.maxvalue([1, 2, 3, 4]) == 4


def testing_minvalue():
    assert utils.minvalue([1, 2, 3, 4]) == 1


def testing_countvalue():
    assert utils.countvalue([1, 2, 3, 4, 4], 4) == 2


def testing_meanvalue():
    assert utils.meannvalue([1, 2, 3, 4, 5]) == 3


