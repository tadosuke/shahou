"""ボールを飛ばす力."""


class Power:
    """ボールを飛ばす力."""

    #: 最大値
    max = 100
    #: 増加の速さ
    speed = 1.0

    def __init__(self, x: int = 0, y: int = 0):
        #: 縦パワー
        self.x = 0
        #: 横パワー
        self.y = 0

    def reset(self):
        """リセット."""
        self.x = 0
        self.y = 0

    def increase_x(self):
        """縦パワーを増加させる."""
        self.x += Power.speed
        if Power.max < self.x:
            self.x = 0

    def increase_y(self):
        """横パワーを増加させる."""
        self.y += Power.speed
        if Power.max < self.y:
            self.y = 0

    @property
    def ratio(self) -> tuple[float, float]:
        """X, Yの割合(0.0～1.0)."""
        rx = float(self.x) / Power.max
        ry = float(self.y) / Power.max
        return rx, ry
