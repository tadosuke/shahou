"""ステージ."""

import random


class Stage:
    """ステージ."""

    #: 風速の範囲
    _WIND_RANGE = (-10, 10)

    def __init__(self, ground_h: int) -> None:
        if ground_h < 0:
            raise ValueError

        #: 風速
        self._wind = 0
        #: 地面の高さ
        self._ground_h = ground_h

    @property
    def wind(self) -> int:
        """風速."""
        return self._wind

    @property
    def ground_h(self) -> int:
        """地面の高さ."""
        return self._ground_h

    def reset_wind(self) -> None:
        """風速を再設定する."""
        (min_, max_) = Stage._WIND_RANGE
        self._wind = random.randint(min_, max_)
