"""valuesモジュールのテスト."""

import unittest

from shahou.app.model.values import (
    Timer,
    Score,
    Size,
    Position,
    Ratio,
)


class TestRatio(unittest.TestCase):

    def test_case(self):
        ratio = Ratio(0.5)
        self.assertAlmostEqual(ratio.ratio, 0.5)
        self.assertEqual(ratio, Ratio(0.5))
        self.assertEqual(ratio, 0.5)
        self.assertEqual(ratio * 1.2, 0.6)


class TestPosition(unittest.TestCase):

    def test_case(self):
        pos = Position(10, 20)
        self.assertEqual(pos.x, 10)
        self.assertEqual(pos.y, 20)
        self.assertEqual(pos.get(), (10, 20))

        pos = pos.move(5, 6)
        self.assertEqual(pos.get(), (15, 26))  # 取り出して比較
        self.assertTrue(pos == (15, 26))  # タプルとの比較
        self.assertTrue(pos == Position(15, 26))  # Positionとの比較


class TestSize(unittest.TestCase):

    def test_case(self):
        size = Size(10, 20)
        self.assertEqual(size.width, 10)
        self.assertEqual(size.height, 20)
        self.assertEqual(size.get(), (10, 20))


class TestTimer(unittest.TestCase):

    def test_case(self):
        timer = Timer(2)
        self.assertAlmostEqual(timer.time, 2)
        self.assertFalse(timer.is_end())

        timer.update(0.5)
        self.assertAlmostEqual(timer.time, 1.5)
        self.assertFalse(timer.is_end())

        timer.update(2)
        self.assertAlmostEqual(timer.time, 0)
        self.assertTrue(timer.is_end())


class TestScore(unittest.TestCase):

    def test_case(self):
        score: Score = Score(10)
        self.assertEqual(score, 10)

        score.add(Score(5))
        self.assertEqual(score.value, 15)
