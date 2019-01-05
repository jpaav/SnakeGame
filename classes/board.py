import random
from enum import Enum

import numpy as np

import pygame as pg


class BoardStates(Enum):
	EMPTY = 0
	APPLE = 1


class Board:

	def __init__(self, screen_dimensions, x_tiles=16, y_tiles=16):
		self.x_tiles = x_tiles
		self.y_tiles = y_tiles
		self.tiles = np.array([[BoardStates.EMPTY] * x_tiles] * y_tiles)
		self.screen_dimensions = screen_dimensions
		self.image_empty = pg.image.load("resources/board_empty_nogridlines.png")
		# self.image_empty = pg.image.load("resources/board_empty_gridlines.png")
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

	def update_board(self, snake, score):
		# Checks if the snake has been spawned
		if len(snake.segments) > 0:
			# Checks if the snake's head is in a board tile with an apple
			head_pos = (snake.segments[0].tile[0], snake.segments[0].tile[1])
			try:
				if self.tiles[head_pos[0]][head_pos[1]] == BoardStates.APPLE:
					# Eat the apple
					snake.grow()
					# Remove the apple from the board
					self.tiles[head_pos[0]][head_pos[1]] = BoardStates.EMPTY
					# Add to score
					score += 1
			# Make sure that the program doesn't crash if head is out of bounds (this is handled elsewhere)
			except IndexError:
				pass
			# Handle snake collision with self
			tiles_dict = {}
			for segment in snake.segments:
				if str(segment.tile) in tiles_dict:
					snake.kill()
				else:
					tiles_dict[str(segment.tile)] = 1
			#  Handle snake's collisions with edge
			x = snake.segments[0].tile[0]
			y = snake.segments[0].tile[1]

			if x > self.x_tiles-1 or x < 0:
				snake.kill()
			if y > self.y_tiles-1 or y < 0:
				snake.kill()
			return score

	def draw(self, screen):
		for col_index, tile_col in enumerate(self.tiles):
			for row_index, tile in enumerate(tile_col):
				if tile == BoardStates.EMPTY:
					screen.blit(self.image_empty, (self.tile_size() * col_index, self.tile_size() * row_index))
				elif tile == BoardStates.APPLE:
					screen.blit(self.image_apple, (self.tile_size() * col_index, self.tile_size() * row_index))

	def clear(self):
		self.tiles = np.array([[BoardStates.EMPTY] * self.x_tiles] * self.y_tiles)

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
