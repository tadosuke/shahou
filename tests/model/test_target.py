"""targetモジュールのテスト."""

import unittest

from shahou.app.model.target import Target
from shahou.app.model.values import Position, Size


class TestTarget(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.target = Target(
            size=Size(20, 60),
            min_pos=Position(150, 100),
            max_pos=Position(350, 200))

    def test_init(self):
        self.assertEqual(self.target.size, Size(20, 60))
        self.assertEqual(self.target.position, Position(0, 0))

    def test_is_hit(self):
        self.target._pos = Position(10, 20)
        (w, h) = self.target.size.get()
        self.assertTrue(self.target.is_hit(Position(10, 20)))
        self.assertFalse(self.target.is_hit(Position(9, 19)))
        self.assertTrue(self.target.is_hit(Position(10 + w, 20 + h)))
        self.assertFalse(self.target.is_hit(Position(11 + w, 21 + h)))
