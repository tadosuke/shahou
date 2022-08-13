from model.game import Game
from view.game_pygame import GameView


# from view.game_pyxel import GameView


def main() -> None:
    """メイン関数."""
    game = Game()
    view = GameView()
    view.run(game)


if __name__ == "__main__":
    main()
