"""game_pygameモジュールのテスト."""

import unittest
import time

import pygame

from shahou.app.model.ball import PowerRatio, Ball
from shahou.app.model.stage import Stage
from shahou.app.model.target import Target
from shahou.app.model.power import Power
from shahou.app.model.values import Position, Size
from shahou.app.view.game_pygame import GameView, PowerView, StageView, BallView, TargetView


class TestGameView(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.view = GameView()

    def test_init(self):
        self.assertIsNotNone(self.view._screen)

    def test_draw_power(self):
        power = Power(50, 60)
        power_view = PowerView(self.view._screen)
        power_view.draw(power)
        pygame.display.update()
        time.sleep(0.5)

    def test_draw_stage(self):
        stage = Stage(ground_h=20)
        stage_view = StageView(self.view._screen)
        stage_view.draw(stage)
        pygame.display.update()
        time.sleep(0.5)

    def test_draw_ball(self):
        ball = Ball(
            size=5,
            power_ratio=PowerRatio(0.1, 0.1),
            gravity=0.5,
            wind_rate=0.1)
        ball.move_to(Position(self.view.SCR_W/2, self.view.SCR_H/2))
        ball_view = BallView(self.view._screen)
        ball_view.draw(ball)
        pygame.display.update()
        time.sleep(0.5)

    def test_draw_target(self):
        target = Target(
            size=Size(20, 60),
            min_pos=Position(100, 100),
            max_pos=Position(100, 100))
        target.move_random()
        target_view = TargetView(self.view._screen)
        target_view.draw(target)
        pygame.display.update()
        time.sleep(0.5)
