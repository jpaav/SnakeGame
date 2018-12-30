from enum import Enum

import pygame as pg

import numpy as np


class Segment(pg.sprite.Sprite):
	def __init__(self, segment_type, tile, velocity, width=16, height=16):
		# Call Sprite constructor
		super().__init__()
		# Init segment
		self.tile = tile
		x = tile[0]*np.linalg.norm(velocity)
		y = tile[1]*np.linalg.norm(velocity)
		self.position = np.array([x, y])
		self.width = width
		self.height = height
		self.velocity = velocity
		self.type = segment_type
		# Set picture according to type
		self.image = None
		self.set_type(segment_type)

	def __str__(self):
		return str(self.position)

	def draw(self, screen, draw_velocities):
		screen.blit(self.image, self.position)
		if draw_velocities:
			self.image.fill([255, 255, 255])
			font = pg.font.SysFont('Comic Sans MS', 10)
			velocity_text = font.render(str(self.velocity), True, (0, 0, 0))
			self.image.blit(velocity_text, (0, 0))

	def move(self, new_velocity=None, new_type=None):
		# Update position
		self.position += self.velocity
		# Update tile
		self.tile += self.normalized_velocity()
		# Change velocity if new one is supplied
		if new_velocity is not None:
			self.velocity = new_velocity
		# Change segment type if new one is supplied
		if new_type is not None and new_type != self.type:
			self.set_type(new_type)

	def turn_left(self):
		if self.velocity[0] != 0 and self.velocity[1] != 0:
			print("Error in Segment.turn_left(): invalid velocity with diagonal direction.")
		elif self.velocity[0] != 0:
			self.velocity = np.array([0, self.velocity[0]])
		elif self.velocity[1] != 0:
			self.velocity = np.array([-self.velocity[1], 0])

	def turn_right(self):
		if self.velocity[0] != 0 and self.velocity[1] != 0:
			print("Error in Segment.turn_right(): invalid velocity with diagonal direction.")
		elif self.velocity[0] != 0:
			self.velocity = np.array([0, -self.velocity[0]])
		elif self.velocity[1] != 0:
			self.velocity = np.array([self.velocity[1], 0])

	def set_type(self, new_type):
		self.type = new_type
		if self.type == SegmentTypes.HEAD:
			self.image = pg.image.load("resources/head.png").convert()
		elif self.type == SegmentTypes.TAIL:
			self.image = pg.image.load("resources/tail.png").convert()
		elif self.type == SegmentTypes.BODY_STRAIGHT:
			self.image = pg.image.load("resources/straight.png").convert()
		elif self.type == SegmentTypes.BODY_LEFT:
			self.image = pg.image.load("resources/left.png").convert()
		elif self.type == SegmentTypes.BODY_RIGHT:
			self.image = pg.image.load("resources/right.png").convert()
		else:
			self.image = pg.image.load("resources/error.png").convert()
			print("type argument should be a SegmentTypes instance")
		# Scale image to be proper dimensions according to class variables
		self.image = pg.transform.scale(self.image, (self.width, self.height))

	def normalized_velocity(self):
		mag = np.linalg.norm(self.velocity)
		return np.array([int(self.velocity[0] / mag), int(self.velocity[1] / mag)])


class SegmentTypes(Enum):
	HEAD = 0
	TAIL = 1
	BODY_STRAIGHT = 2
	BODY_RIGHT = 3
	BODY_LEFT = 4
