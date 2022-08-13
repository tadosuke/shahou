"""gameモジュールのテスト."""

import unittest

from shahou.app.model.game import (
    Game,
    Mode,
)

from shahou.app.model.values import Timer


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_init(self):
        self.assertEqual(self.game.time, 0)
        self.assertEqual(self.game._mode, Mode.INIT)
        self.assertEqual(self.game._wait_timer.time, 0)
        self.assertEqual(self.game.score.value, 0)
        self.assertFalse(self.game._decide)
        self.assertIsNotNone(self.game._ball)
        self.assertIsNotNone(self.game.target)
        self.assertIsNotNone(self.game.stage)

    def test_send_decide(self):
        self.game.send_decide()
        self.assertTrue(self.game._decide)
        self.game.update(0.5)
        self.assertFalse(self.game._decide)

    def test_balltime_to_score(self):
        self.game._ball._time = 5
        self.assertEqual(self.game._balltime_to_score(), 5)
