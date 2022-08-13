"""ゲームモデル."""

from __future__ import annotations

from enum import Enum

from shahou.app.model.ball import Ball, PowerRatio
from shahou.app.model.power import Power
from shahou.app.model.stage import Stage
from shahou.app.model.target import Target
from shahou.app.model.values import (
    Timer,
    Score,
    Size,
    Position,
    Ratio,
)


class Mode(Enum):
    """ゲームモード."""

    INIT = 0  # 初期
    POW_X = 1  # Xパワー決定待ち
    POW_Y = 2  # Yパワー決定待ち
    FLYING = 3  # 飛行中
    WAIT_HIT = 4  # ヒット演出中
    WAIT_OUT = 5  # 外れ演出中
    TIME_UP = 6  # 時間切れ演出中
    RESULT = 7  # リザルト


class Game:
    """ゲーム本体."""

    #: 制限時間
    _MAX_TIME: float = 60
    #: ヒット演出時間
    _WAIT_TIME_HIT: float = 1.0
    #: タイムアップ演出時間
    _WAIT_TIME_END: float = 2.0

    #: 的の最小位置
    _TARGET_POS_MIN: Position = Position(150, 100)
    #: 的の最大位置
    _TARGET_POS_MAX: Position = Position(350, 200)
    #: 的のサイズ
    _TARGET_SIZE: Size = Size(20, 80)

    #: ボール初期位置
    _BALL_POS_INIT: Position = Position(20, 25)
    #: ボールサイズ
    _BALL_SIZE: int = 6
    #: ボールにかかる重力
    _BALL_GRAVITY: float = 0.4
    #: 風の適用率
    _BALL_WIND_RATE: Ratio = Ratio(0.01)
    #: パワーの適用率
    _BALL_POWER_RATIO: PowerRatio = PowerRatio(0.08, 0.2)

    #: 地面の高さ
    _GROUND_H: int = 20

    def __init__(self) -> None:
        self._stage = Stage(Game._GROUND_H)
        self._target = Target(
            size=Game._TARGET_SIZE,
            min_pos=Game._TARGET_POS_MIN,
            max_pos=Game._TARGET_POS_MAX)
        self._power: Power = Power()
        self._timer: Timer = Timer(0)
        self._wait_timer: Timer = Timer(0)  # 演出タイマー
        self._reset()
        self._mode = Mode.INIT  # モード番号
        self._decide = False  # 決定操作がされたか
        self._score = Score(0)

        # update関数テーブル
        self.update_dictionary = {
            Mode.INIT: self._update_init,
            Mode.POW_X: self._update_pow_x,
            Mode.POW_Y: self._update_pow_y,
            Mode.FLYING: self._update_flying,
            Mode.WAIT_HIT: self._update_wait_hit,
            Mode.WAIT_OUT: self._update_wait_out,
            Mode.TIME_UP: self._update_timeup,
            Mode.RESULT: self._update_result,
        }

    @property
    def score(self) -> Score:
        """スコア."""
        return self._score

    @property
    def time(self) -> float:
        """残り時間."""
        return self._timer.time

    @property
    def target(self) -> Target:
        """的."""
        return self._target

    @property
    def stage(self) -> Stage:
        """ステージ."""
        return self._stage

    @property
    def power(self) -> Power:
        """パワー."""
        return self._power

    @property
    def ball(self) -> Ball:
        """ボール."""
        return self._ball

    def _reset(self) -> None:
        """状態をリセットする."""
        self._ball = Ball(
            size=Game._BALL_SIZE,
            power_ratio=Game._BALL_POWER_RATIO,
            gravity=Game._BALL_GRAVITY,
            wind_rate=Game._BALL_WIND_RATE)
        self._ball.reset(Game._BALL_POS_INIT)
        self._power.reset()
        self._stage.reset_wind()
        self._target.move_random()

    def _update_init(self, delta: float) -> None:
        """更新：初期設定."""
        self._reset()
        self._score = Score(0)
        self._timer = Timer(Game._MAX_TIME)
        self._mode = Mode.POW_X

    def _update_pow_x(self, delta: float) -> None:
        """更新：横パワー決定待ち."""
        # 残り時間更新
        self._timer.update(delta)
        if self._timer.is_end():
            self._wait_timer = Timer(Game._WAIT_TIME_END)
            self._mode = Mode.TIME_UP
        # 横パワー更新
        else:
            self._power.increase_x()
            if self._decide:
                self._mode = Mode.POW_Y

    def _update_pow_y(self, delta: float) -> None:
        """更新：縦パワー決定待ち."""
        # 残り時間更新
        self._timer.update(delta)
        if self._timer.is_end():
            self._wait_timer = Timer(Game._WAIT_TIME_END)
            self._mode = Mode.TIME_UP
        # 縦パワー更新
        else:
            self._power.increase_y()
            if self._decide:
                self._ball.kick(self._power.x, self._power.y)
                self._mode = Mode.FLYING

    def _update_flying(self, delta: float) -> None:
        """更新：ボール飛行中."""
        self._ball.update(delta, self._stage.wind)

        # 的に接触
        if self._target.is_hit(self._ball.pos):
            self._wait_timer = Timer(Game._WAIT_TIME_HIT)
            self._mode = Mode.WAIT_HIT
        # 地面に接触
        elif self._is_ball_on_ground(self._ball):
            self._ball.attach_bottom(Game._GROUND_H)
            self._wait_timer = Timer(Game._WAIT_TIME_HIT)
            self._mode = Mode.WAIT_OUT

    @staticmethod
    def _is_ball_on_ground(ball: Ball):
        """ボールが地面に触れたか."""
        return ball.bottom <= Game._GROUND_H

    def _update_wait_hit(self, delta: float) -> None:
        """更新：ヒット演出待ち."""
        self._wait_timer.update(delta)
        if self._wait_timer.is_end():
            self._score.add(self._balltime_to_score())
            self._reset()
            self._mode = Mode.POW_X

    def _balltime_to_score(self) -> Score:
        """ボールの滞空時間からスコアを得る."""
        return Score(int(self._ball.time))

    def _update_wait_out(self, delta: float) -> None:
        """更新：外れ演出待ち."""
        self._wait_timer.update(delta)
        if self._wait_timer.is_end():
            self._reset()
            self._mode = Mode.POW_X

    def _update_timeup(self, delta: float) -> None:
        """更新：タイムアップ演出待ち."""
        self._wait_timer.update(delta)
        if self._wait_timer.is_end():
            self._wait_timer = Timer(0)
            self._mode = Mode.RESULT

    def _update_result(self, delta: float) -> None:
        """更新：リザルト."""
        if self._decide:
            self._mode = Mode.INIT

    def update(self, delta: float) -> None:
        """更新."""
        func = self.update_dictionary[self._mode]
        func(delta)

        self._decide = False

    def send_decide(self) -> None:
        """決定操作."""
        self._decide = True

    def is_flying(self) -> bool:
        """ボール飛行中か."""
        return self._mode == Mode.FLYING

    def is_hit(self) -> bool:
        """ヒット演出中か."""
        return self._mode == Mode.WAIT_HIT

    def is_timeup(self) -> bool:
        """時間切れか."""
        return self._mode == Mode.TIME_UP

    def is_result(self) -> bool:
        """リザルト表示中か."""
        return self._mode == Mode.RESULT
