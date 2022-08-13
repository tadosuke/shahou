"""ballモジュールのテスト."""

import unittest

from shahou.app.model.ball import Ball, PowerRatio
from shahou.app.model.values import Position, Ratio


class TestPowerRatio(unittest.TestCase):

    def test_case(self):
        ratio = PowerRatio(0.5, 0.8)
        self.assertAlmostEqual(ratio.x, 0.5)
        self.assertAlmostEqual(ratio.y, 0.8)
        self.assertAlmostEqual(ratio * (2.0, 0.5), (1.0, 0.4))


class TestBall(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.ball = Ball(
            size=5,
            power_ratio=PowerRatio(Ratio(0.1), Ratio(0.2)),
            gravity=0.4,
            wind_rate=0.1)

    def test_init(self) -> None:
        self.assertEqual(self.ball.pos, Position(0, 0))
        self.assertEqual(self.ball.sx, 0)
        self.assertEqual(self.ball.sy, 0)
        self.assertEqual(self.ball.time, 0)

    def test_reset(self) -> None:
        self.ball.reset(Position(10, 20))
        self.assertEqual(self.ball.pos, Position(10, 20))
        self.assertEqual(self.ball.sx, 0)
        self.assertEqual(self.ball.sy, 0)
        self.assertEqual(self.ball.time, 0)

    def test_kick(self) -> None:
        self.ball.kick(30, 60)
        self.assertEqual(self.ball._power_ratio.x * 30, self.ball.sx)
        self.assertEqual(self.ball._power_ratio.y * 60, self.ball.sy)
        self.assertEqual(self.ball.time, 0)

    def test_update(self) -> None:
        # 無風
        self.ball.reset()
        self.ball.kick(50, 40)
        sx = self.ball.sx
        sy = self.ball.sy
        self.ball.update(1, 0)
        self.assertEqual(self.ball.sx, sx)
        self.assertEqual(self.ball.sy, sy - self.ball._gravity)
        self.assertEqual(self.ball.time, 10)

        # 順風
        self.ball.reset()
        self.ball.kick(50, 40)
        sx = self.ball.sx
        self.ball.update(1, 5)
        self.assertEqual(self.ball.sx, sx + 5 * self.ball._wind_rate)

        # 逆風
        self.ball.reset()
        self.ball.kick(50, 40)
        sx = self.ball.sx
        self.ball.update(1, -5)
        self.assertEqual(self.ball.sx, sx - 5 * self.ball._wind_rate)
