# main.py in the root directory
import sys
from view.game_view import GameView

def main():
    game_view = GameView()
    game_view.main_loop()

if __name__ == "__main__":
    main()
