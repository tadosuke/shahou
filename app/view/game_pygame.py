"""ゲームビュー（pygame）.

pygameは左上原点
"""

import time

import pygame

from shahou.app.model.game import Game
from shahou.app.model.stage import Stage
from shahou.app.model.power import Power
from shahou.app.model.ball import Ball
from shahou.app.model.target import Target


class IView:
    """ビューの基底クラス."""
    def __init__(self, screen: pygame.Surface):
        self._screen = screen

    def draw(self, obj: object):
        """描画."""
        pass

    @property
    def screen(self) -> pygame.Surface:
        """スクリーン."""
        return self._screen


class BallView(IView):
    """ボール."""

    _COLOR = (255, 255, 255)

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

    def draw(self, ball: Ball) -> None:
        """描画."""
        ball_center_pos = (ball.pos.x, GameView.SCR_H - ball.pos.y)
        pygame.draw.circle(self.screen, self._COLOR, ball_center_pos, ball.size)


class PowerView(IView):
    """パワーゲージ."""

    _COLOR_X = (0, 255, 0)
    _COLOR_Y = (255, 0, 0)
    _HEIGHT = 10

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

    def draw(self, power: Power) -> None:
        """描画."""
        rx, ry = power.ratio

        # 横ゲージ
        pow_x_rect = pygame.Rect(
            0,
            GameView.SCR_H - self._HEIGHT * 2,
            rx * GameView.SCR_W,
            self._HEIGHT)
        pygame.draw.rect(self.screen, self._COLOR_X, pow_x_rect)

        # 縦ゲージ
        pow_y_rect = pygame.Rect(
            0,
            GameView.SCR_H - self._HEIGHT,
            ry * GameView.SCR_W,
            self._HEIGHT)
        pygame.draw.rect(self.screen, self._COLOR_Y, pow_y_rect)


class StageView(IView):
    """ステージ."""

    _BG_COLOR = (80, 255, 255)
    _GROUND_COLOR = (80, 0, 0)

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

    def draw(self, stage: Stage) -> None:
        """描画."""
        # 背景
        self.screen.fill(self._BG_COLOR)

        # 地面
        ground_rect = pygame.Rect(0, GameView.SCR_H - stage.ground_h, GameView.SCR_W, stage.ground_h)
        pygame.draw.rect(self.screen, self._GROUND_COLOR, ground_rect)


class TargetView(IView):
    """的."""

    _COLOR = (0, 0, 255)

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

    def draw(self, target: Target) -> None:
        """描画."""
        (x, y) = target.position.get()
        (w, h) = target.size.get()
        target_rect = pygame.Rect(
            x,
            GameView.SCR_H - h - y,
            w,
            h)
        pygame.draw.rect(self.screen, self._COLOR, target_rect)


class ResultView(IView):
    """リザルト画面."""

    #: デフォルトのテキストカラー(RGB)
    _TEXT_COLOR_NORMAL = (255, 255, 255)

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self._font_m = pygame.font.Font(None, 24)
        self._font_l = pygame.font.Font(None, 48)

    def draw(self, game: Game) -> None:
        """描画."""
        # 背景
        bg_color = (0, 0, 0)
        self.screen.fill(bg_color)

        # 見出し
        caption_text = "Score"
        (caption_text_w, caption_text_h) = self._font_l.size(caption_text)
        caption_render = self._font_l.render(caption_text, True, self._TEXT_COLOR_NORMAL)
        caption_pos = [GameView.SCR_W / 2 - caption_text_w / 2, GameView.SCR_H / 2 - caption_text_h / 2]
        self.screen.blit(caption_render, caption_pos)

        # スコア
        score_text = str(game.score)
        (score_text_w, score_text_h) = self._font_l.size(score_text)
        score_render = self._font_l.render(score_text, True, self._TEXT_COLOR_NORMAL)
        score_pos = [GameView.SCR_W / 2 - score_text_w / 2, GameView.SCR_H / 2 + score_text_h / 2]
        self.screen.blit(score_render, score_pos)


class GameView:
    """ゲームビュー."""

    #: スクリーン幅
    SCR_W = 400
    #: スクリーン高さ
    SCR_H = 300
    #: デフォルトのテキストカラー(RGB)
    _TEXT_COLOR_NORMAL = (255, 255, 255)

    def __init__(self):
        pygame.init()
        self._screen: pygame.Surface = pygame.display.set_mode((GameView.SCR_W, GameView.SCR_H))
        pygame.display.set_caption("Shahou-Shusha")

        # メンバー変数
        self._is_click = False
        self._font_m = pygame.font.Font(None, 24)
        self._font_l = pygame.font.Font(None, 48)

        self._main_views = (
            StageView(self._screen),
            TargetView(self._screen),
            BallView(self._screen),
            PowerView(self._screen))
        self._result_view: ResultView = ResultView(self._screen)

    def run(self, game: Game) -> None:
        """起動."""
        running = True
        while running:
            delta_sec = 1.0 / 60.0
            game.update(delta_sec)
            self._draw(game)
            running = self._process_event(game)
            time.sleep(delta_sec)

    def _draw(self, game: Game) -> None:
        """描画."""
        if game.is_result():
            self._result_view.draw(game)
        else:
            objects = (game.stage, game.target, game.ball, game.power)
            for view, obj in zip(self._main_views, objects):
                view.draw(obj)
            self._draw_texts(game)

        pygame.display.update()

    def _draw_texts(self, game: Game) -> None:
        """描画：テキスト."""
        # スコア
        score_text = "Score = " + str(game.score)
        score_pos = [5, 10]
        score_render = self._font_m.render(score_text, True, GameView._TEXT_COLOR_NORMAL)
        self._screen.blit(score_render, score_pos)

        # 時間
        time_text = "Time = " + str(int(game.time))
        time_pos = [5, 34]
        time_render = self._font_m.render(time_text, True, GameView._TEXT_COLOR_NORMAL)
        self._screen.blit(time_render, time_pos)

        # 風
        wind_text = "Wind = " + str(int(game.stage.wind))
        wind_pos = [5, 58]
        wind_render = self._font_m.render(wind_text, True, GameView._TEXT_COLOR_NORMAL)
        self._screen.blit(wind_render, wind_pos)

        # 滞空時間
        if game.is_flying() or game.is_hit():
            flying_text = str(int(game._ball._time))
            flying_pos = [100, 10]
            flying_color = (0, 0, 255)
            flying_render = self._font_m.render(flying_text, True, flying_color)
            self._screen.blit(flying_render, flying_pos)

        # Hit
        if game.is_hit():
            hit_text = "HIT!"
            (hit_text_w, hit_text_h) = self._font_l.size(hit_text)
            hit_pos = [GameView.SCR_W / 2 - hit_text_w / 2, GameView.SCR_H / 2 - hit_text_h / 2]
            hit_color = (255, 0, 0)
            hit_render = self._font_l.render(hit_text, True, hit_color)
            self._screen.blit(hit_render, hit_pos)

        # TimeUp
        if game.is_timeup():
            time_up_text = "Time up!"
            (time_up_text_w, time_up_text_h) = self._font_l.size(time_up_text)
            time_up_pos = (GameView.SCR_W / 2 - time_up_text_w / 2, GameView.SCR_H / 2 - time_up_text_h / 2)
            time_up_color = (255, 0, 0)
            time_up_render = self._font_l.render(time_up_text, True, time_up_color)
            self._screen.blit(time_up_render, time_up_pos)

    def _process_event(self, game: Game) -> bool:
        """イベント処理."""
        for event in pygame.event.get():
            # マウスクリック
            (btn1, btn2, btn3) = pygame.mouse.get_pressed()
            if btn1:
                if not self._is_click:
                    game.send_decide()
                    self._is_click = True
            else:
                self._is_click = False

            # 終了イベント
            if event.type == pygame.QUIT:
                pygame.quit()  # pygameのウィンドウを閉じる
                return False

        return True
