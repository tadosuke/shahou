"""powerモジュールのテスト."""

import unittest

from shahou.app.model.power import Power


class TestPower(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.power = Power()

    def test_init(self):
        self.assertEqual(self.power.x, 0)
        self.assertEqual(self.power.y, 0)

    def test_reset(self):
        self.power.increase_x()
        self.power.increase_y()
        self.power.reset()
        self.assertEqual(self.power.x, 0)
        self.assertEqual(self.power.y, 0)

    def test_increase(self):
        self.power.increase_x()
        self.assertAlmostEqual(self.power.x, Power.speed)

        self.power.increase_y()
        self.power.increase_y()
        self.assertAlmostEqual(self.power.y, Power.speed * 2)
