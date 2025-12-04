"""
Главный файл игры
"""

import pygame
import sys
from game import Game

def main():
    try:
        pygame.init()
        game = Game()
        game.run()
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()