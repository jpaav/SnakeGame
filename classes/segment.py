from enum import Enum

import pygame as pg


class Segment(pg.sprite.Sprite):
	def __init__(self, segment_type, position=(0, 0), width=16, height=16):
		# Call Sprite constructor
		super().__init__()
		# Init segment
		self.position = position
		self.width = width
		self.height = height
		self.type = segment_type
		# Set picture according to type
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

	@staticmethod
	def subtract_tuples(tuple1, tuple2):
		return tuple1[0] - tuple2[0], tuple1[1] - tuple2[1]

	def __str__(self):
		return str(self.position)

	def draw(self, screen):
		screen.blit(self.image, self.position)


class SegmentTypes(Enum):
	HEAD = 0
	TAIL = 1
	BODY_STRAIGHT = 2
	BODY_RIGHT = 3
	BODY_LEFT = 4
