"""ボール."""

from shahou.app.model.values import Position, Ratio

from dataclasses import dataclass


@dataclass
class PowerRatio:
    x: Ratio
    y: Ratio

    def __init__(self, x, y) -> None:
        if isinstance(x, Ratio):
            self.x = x
        else:
            self.x = Ratio(x)

        if isinstance(x, Ratio):
            self.y = y
        else:
            self.y = Ratio(y)

    def __mul__(self, value: tuple[float, float]) -> tuple[float, float]:
        """乗算."""
        (x, y) = value
        return self.x * x, self.y * y


class Ball:
    """ボール."""

    def __init__(self,
                 size: int,
                 power_ratio: PowerRatio,
                 gravity: float,
                 wind_rate: Ratio) -> None:
        self._pos = Position(0, 0)
        self.sx: float = 0
        self.sy: float = 0
        self._time: float = 0

        if size <= 0:
            raise ValueError
        if gravity <= 0:
            raise ValueError

        #: サイズ
        self._size = size
        #: ボールにかかる重力
        self._gravity = gravity
        #: 風の適用率
        self._wind_rate = wind_rate
        self._power_ratio: PowerRatio = power_ratio

    @property
    def pos(self) -> Position:
        return self._pos

    @property
    def size(self) -> int:
        return self._size

    @property
    def bottom(self) -> float:
        """下端の位置."""
        return self._pos.y - self._size

    @property
    def time(self) -> int:
        """飛行時間."""
        return int(self._time)

    def attach_bottom(self, y: int):
        """下端がyになるように移動する."""
        self._pos = Position(self._pos.x, y + self.size)

    def move_to(self, position: Position) -> None:
        """移動."""
        self._pos = position

    def reset(self, position: Position = Position(0, 0)) -> None:
        """リセット."""
        self._pos = position
        self.sx = 0  # X速さ
        self.sy = 0  # Y速さ
        self._time = 0  # 飛行時間

    def kick(self, pow_x: float, pow_y: float) -> None:
        """キック."""
        self.sx, self.sy = self._power_ratio * (pow_x, pow_y)
        self._time = 0

    def update(self, delta: float, wind: float) -> None:
        """更新."""
        self.sx += self._wind_rate * wind
        self.sy -= self._gravity
        self._pos = self._pos.move(self.sx, self.sy)
        self._time += delta * 10
