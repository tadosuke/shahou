import pyxel
from shahou.app.model.game import Game


# =======================================================
# ゲームビュー（pyxel）
# =======================================================
class GameView:
    scr_w = 160
    scr_h = 120
    gage_h = 4

    # -------------------------------------------------------
    # コンストラクタ
    # -------------------------------------------------------
    def __init__(self) -> None:
        pyxel.init(GameView.scr_w, GameView.scr_h, caption="Shahou-shusha", fps=60)

    # -------------------------------------------------------
    # 起動
    # -------------------------------------------------------
    def run(self, game: Game) -> None:
        self.game = game
        self.scr_ratio_w = GameView.scr_w / Game.world_w  # 画面幅比率
        self.scr_ratio_h = GameView.scr_h / Game.world_h  # 画面高さ比率
        pyxel.run(self.update, self.draw)

    # -------------------------------------------------------
    # 更新
    # -------------------------------------------------------
    def update(self) -> None:
        self.game.update(1.0 / 60.0)

        # クリック
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.game.send_decide()

        # 終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    # -------------------------------------------------------
    # 描画
    #   pyxelでは画面左上が(0, 0)になる
    # -------------------------------------------------------
    def draw(self) -> None:
        # リザルト
        if self.game.is_result():
            self.draw_result()
            return

        pyxel.cls(12)

        # 地面
        ground_y = GameView.scr_h - (self.game._GROUND_H * self.scr_ratio_h)
        ground_h = Game._GROUND_H * self.scr_ratio_h
        pyxel.rect(0, ground_y, GameView.scr_w, ground_h, 4)

        # 横ゲージ
        gage_x_y = GameView.scr_h - GameView.gage_h * 2
        gage_x_w = self.game.get_pow_x_ratio() * GameView.scr_w
        pyxel.rect(0, gage_x_y, gage_x_w, GameView.gage_h, 11)

        # 縦ゲージ
        gage_y_y = GameView.scr_h - GameView.gage_h
        gage_y_w = self.game.get_pow_y_ratio() * GameView.scr_w
        pyxel.rect(0, gage_y_y, gage_y_w, GameView.gage_h, 8)

        # 的
        target_x = self.game.target.x * self.scr_ratio_w
        target_y = GameView.scr_h - (self.game.target.y * self.scr_ratio_h)
        target_w = self.game.target_w * self.scr_ratio_w
        target_h = self.game.target_h * self.scr_ratio_h
        pyxel.rect(target_x, target_y, target_w, target_h, 5)

        # ボール
        ball_x = self.game._ball.x * self.scr_ratio_w
        ball_y = GameView.scr_h - (self.game._ball.y * self.scr_ratio_h)
        ball_size = self.game._BALL_SIZE * self.scr_ratio_h
        pyxel.circ(ball_x, ball_y, ball_size, 7)

        # スコア
        pyxel.text(0, 0, "Score = " + str(int(self.game.score)), 7)

        # 残り時間
        pyxel.text(0, 10, "Time = " + str(int(self.game.time)), 7)

        # 風
        pyxel.text(0, 20, "Wind = " + str(int(self.game.stage._wind)), 7)

        # 滞空時間
        if self.game.is_flying() or self.game.is_hit():
            pyxel.text(50, 0, str(int(self.game._ball.time)), 1)

        # ヒット
        if self.game.is_hit():
            pyxel.text(GameView.scr_w / 2 - 13, GameView.scr_h / 2, "HIT!", 8)

        # タイムアップ
        if self.game.is_timeup():
            pyxel.text(GameView.scr_w / 2 - 15, GameView.scr_h / 2, "Time up!", 8)

    # -------------------------------------------------------
    # 描画：リザルト
    # -------------------------------------------------------
    def draw_result(self) -> None:
        pyxel.cls(0)

        # スコア
        pyxel.text(GameView.scr_w / 2 - 22, GameView.scr_h / 2, "Score = " + str(int(self.game.score)), 7)
