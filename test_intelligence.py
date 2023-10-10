import pytest
import numpy as np
import intelligence


def test_enqueue():
    q = np.array([])
    t = intelligence.enqueue(q, "test")
    assert t[0] == "test"


def test_dequeue():
    q = np.array([1, 2, 3, 4])
    (a, b) = intelligence.dequeue(q)
    assert a == 1, b == [2, 3, 4]


def test_is_empty():
    q = np.array([1, 2, 3, 4])
    assert intelligence.is_empty(q) == False
    for i in range(4):
        (a, s) = intelligence.dequeue(q)
        q = s
    assert intelligence.is_empty(q) == True
