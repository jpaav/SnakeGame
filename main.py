import sys

import pygame as pg

from logic import game
if __name__ == '__main__':
	snake_game = game.SnakeGame()
	exit_code = snake_game.start()
	pg.quit()
	sys.exit(exit_code)
