"""値オブジェクトたち."""

from __future__ import annotations

import math


class Ratio:
    """割合."""

    def __init__(self, ratio: float) -> None:
        if ratio < 0:
            raise ValueError
        self._ratio: float = ratio

    @property
    def ratio(self) -> float:
        return self._ratio

    def __eq__(self, other) -> bool:
        """等価比較."""
        if isinstance(other, Ratio):
            return math.isclose(self._ratio, other.ratio)
        elif isinstance(other, float):
            return math.isclose(self._ratio, other)
        return False

    def __mul__(self, other):
        """乗算."""
        if isinstance(other, Ratio):
            return self._ratio * other.ratio
        return self._ratio * other


class Position:
    """座標."""

    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        """X座標."""
        return self._x

    @property
    def y(self) -> float:
        """Y座標."""
        return self._y

    def get(self) -> tuple[float, float]:
        """タプルでまとめて取得"""
        return self._x, self._y

    def move(self, x: float, y: float) -> Position:
        """x, yだけ移動した座標を得る."""
        return Position(self._x + x, self._y + y)

    def __eq__(self, other) -> bool:
        """等価比較."""
        if isinstance(other, Position):
            return self._x == other.x and self._y == other.y
        elif isinstance(other, tuple):
            (x, y) = other
            return self._x == x and self._y == y
        return False


class Size:
    """大きさ.

    :param width:
    """

    def __init__(self, width: int, height: int) -> None:
        if width <= 0:
            raise ValueError
        self._width = width

        if height <= 0:
            raise ValueError
        self._height = height

    @property
    def width(self) -> int:
        """幅."""
        return self._width

    @property
    def height(self) -> int:
        """高さ."""
        return self._height

    def get(self) -> tuple[int, int]:
        """タプルでまとめて取得する."""
        return self._width, self._height

    def __eq__(self, other) -> bool:
        """等価比較."""
        if isinstance(other, Size):
            return self._width == other.width and self._height == other.height
        elif isinstance(other, tuple):
            (w, h) = other
            return self._width == w and self._height == h
        return False


class Timer:
    """タイマー.

    :param seconds: 秒数
    """

    def __init__(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError
        self._time = seconds

    def update(self, delta: float) -> None:
        """タイマーの更新."""
        if delta < 0:
            raise ValueError
        self._time -= delta
        self._time = max(self._time, 0)

    @property
    def time(self) -> float:
        """残り時間."""
        return self._time

    def is_end(self) -> bool:
        """終了しているか."""
        return math.isclose(self._time, 0)


class Score:
    """スコア."""

    def __init__(self, score: int) -> None:
        if score < 0:
            raise ValueError
        self._score = score

    def add(self, score: Score) -> None:
        """加算."""
        self._score += score.value

    @property
    def value(self) -> int:
        """値の取得."""
        return self._score

    def __str__(self):
        return str(self._score)

    def __eq__(self, other):
        if isinstance(other, Score):
            return self.value == other.value
        return self.value == other
