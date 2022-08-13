"""的."""

import random

from shahou.app.model.values import Position, Size


class Target:
    """的."""

    def __init__(
            self,
            size: Size,
            min_pos: Position,
            max_pos: Position) -> None:
        self._size = size
        self._min_pos = min_pos
        self._max_pos = max_pos
        self._pos: Position = Position(0, 0)

    @property
    def position(self) -> Position:
        """位置."""
        return self._pos

    @property
    def size(self) -> Size:
        """サイズ."""
        return self._size

    def move_random(self) -> None:
        """位置をランダムで移動させる."""
        self._pos = Position(
            x=random.randint(self._min_pos.x, self._max_pos.x),
            y=random.randint(self._min_pos.y, self._max_pos.y))

    def is_hit(self, position: Position) -> bool:
        """地点（x, y）と衝突しているか."""
        left = self._pos.x
        right = self._pos.x + self._size.width
        top = self._pos.y
        bottom = self._pos.y + self._size.height

        contain_x = (left <= position.x <= right)
        contain_y = (top <= position.y <= bottom)
        if contain_x and contain_y:
            return True
        return False
