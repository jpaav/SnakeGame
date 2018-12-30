import random
from enum import Enum

import numpy as np

import pygame as pg


class BoardStates(Enum):
	EMPTY = 0
	# SNAKE = 1
	APPLE = 2


class Board:

	def __init__(self, screen_dimensions, x_tiles=16, y_tiles=16):
		self.x_tiles = x_tiles
		self.y_tiles = y_tiles
		self.tiles = np.array([[BoardStates.EMPTY] * x_tiles] * y_tiles)
		self.screen_dimensions = screen_dimensions
		self.image_empty = pg.image.load("resources/board_empty.png")
		self.image_apple = pg.image.load("resources/board_apple.png")
		# Scale image to be proper dimensions according to class variables
		self.image_empty = pg.transform.scale(self.image_empty, (self.tile_size(), self.tile_size()))
		self.image_apple = pg.transform.scale(self.image_apple, (self.tile_size(), self.tile_size()))

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
		print("================ DRAW ITERATION ================")
		for col_index, tile_col in enumerate(self.tiles):
			# print("col_index: " + str(col_index))
			for row_index, tile in enumerate(tile_col):
				# print("row_index: " + str(row_index))
				print("tile: " + str(tile))
				if tile == BoardStates.EMPTY:
					screen.blit(self.image_empty, (self.tile_size() * col_index, self.tile_size() * row_index))
				elif tile == BoardStates.APPLE:
					screen.blit(self.image_apple, (self.tile_size() * col_index, self.tile_size() * row_index))
		return

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
