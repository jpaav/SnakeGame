from enum import Enum

import pygame as pg


class Segment(pg.sprite.Sprite):
	position = (0, 0)
	width = 16
	height = 16

	def __init__(self, position, type):
		self.pos = position
		# Call Sprite constructor
		super().__init__()
		self.type = type
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
			self.image =  pg.image.load("resources/error.png").convert()
			print("type argument should be a SegmentTypes instance")



	@staticmethod
	def subtract_tuples(tuple1, tuple2):
		return tuple1[0] - tuple2[0], tuple1[1] - tuple2[1]

	def __str__(self):
		return str(self.position)

	def draw(self):
		pass


class SegmentTypes(Enum):
	HEAD = 0
	TAIL = 1
	BODY_STRAIGHT = 2
	BODY_RIGHT = 3
	BODY_LEFT = 4
