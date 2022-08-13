"""stageモジュールのテスト."""

import unittest

from shahou.app.model.stage import Stage


class TestStage(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.stage = Stage(ground_h=20)

    def test_init(self):
        self.assertEqual(self.stage.ground_h, 20)
        self.assertEqual(self.stage.wind, 0)

    def test_reset_wind(self):
        self.stage.reset_wind()
        (min_, max_) = Stage._WIND_RANGE
        self.assertTrue(min_ <= self.stage.wind <= max_)
