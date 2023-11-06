import unittest
from coord import Coord

class TestCoord(unittest.TestCase):
    def test_eq(self):
        res = Coord(1,2) == Coord(1,2)
        self.assertEqual(res, True)


    def test_add(self):
        res = Coord(1, 0) + (1, 2)
        self.assertEqual(res, Coord(2, 2))
        res = Coord(1, 0) + Coord(1, 2)
        self.assertEqual(res, Coord(2, 2))

    def test_sub(self):
        res = Coord(1, 0) - (1, 2)
        self.assertEqual(res, Coord(0,-2))
        res = Coord(1, 0) - Coord(1, 2)
        self.assertEqual(res, Coord(0,-2))

    def test_iadd(self):
        test = Coord(1,2)
        test += (1,2)
        self.assertEqual(test, Coord(2,4))
        t1 = Coord(0,1)
        t2 = t1
        t1 += t2
        self.assertIs(t1, t2)

    def test_isub(self):
        test = Coord(1,2)
        test -= (1,2)
        self.assertEqual(test, Coord(0,0))

    def test_mult(self):
        res = Coord(1,2) * 3
        self.assertEqual(res, Coord(3,6))
        res = Coord(1,2) * 0.9
        self.assertEqual(res, Coord(0.9, 1.8))

    def test_dev(self):
        res = Coord(3,6) / 2
        self.assertEqual(res, Coord(1.5, 3))

