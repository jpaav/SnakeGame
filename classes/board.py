import random
from enum import Enum

import numpy as np


class BoardStates(Enum):
	EMPTY = 0
	# SNAKE = 1
	APPLE = 2


class Board:

	def __init__(self, screen_dimensions, x_tiles=16, y_tiles=16):
		self.x_tiles = x_tiles
		self.y_tiles = y_tiles
		self.tiles = [[BoardStates.EMPTY] * x_tiles] * y_tiles
		self.screen_dimensions = screen_dimensions

	def spawn_apples(self, count=1):
		# This algorithm may need changing so that it never spawns apples in the snake
		for i in range(count):
			x_tile = random.randint(0, self.x_tiles-1)
			y_tile = random.randint(0, self.y_tiles-1)
			self.tiles[x_tile][y_tile] = BoardStates.APPLE

	def update_board(self, snake):
		old_board = self.tiles

		pass
		# Return true if colliding

	def draw(self, screen):
		pass

	def get_center(self):
		# NOTE: Take margins into account if those get added!!
		tile_size = self.tile_size()
		center_x_tile = int(self.x_tiles/2)
		center_y_tile = int(self.y_tiles/2)
		return np.array([center_x_tile*tile_size, center_y_tile*tile_size])

	def tile_size(self):
		return int(self.screen_dimensions[0]/self.x_tiles)

	def get_center_tile(self):
		return np.array([int(self.x_tiles/2), int(self.y_tiles/2)])
