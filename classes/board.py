import random
from enum import Enum


class BoardStates(Enum):
	EMPTY = 0
	SNAKE = 1
	APPLE = 2


class Board:
	x_tiles = 16
	y_tiles = 16
	tiles = [[BoardStates.EMPTY] * x_tiles] * y_tiles

	def spawn_apples(self, count=1):
		# This algorithm may need changing so that it never spawns apples in the snake
		for i in range(count):
			x_tile = random.randint(0, self.x_tiles-1)
			y_tile = random.randint(0, self.y_tiles-1)
			self.tiles[x_tile][y_tile] = BoardStates.APPLE

	def update_board(self, snake):
		pass
		# Return true if colliding
