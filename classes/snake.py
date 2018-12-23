import copy
import random

import numpy as np

from classes.segment import Segment, SegmentTypes


class Snake:
	alive = True
	# Stores a list of tuples representing where the body currently is
	# Should have length matching length variable
	# First value should be head position, last value should be tail position
	segments = []

	def __init__(self, length=3):
		# Includes head and tail
		self.length = length
		# TODO: Maybe remove this line from __init__?
		# idk its kinda essential and shouldn't be optional but gets called 3 times this way
		# self.set_snake_pos()

		# Instance variable to detect whether the snake should turn next time it moves
		self.should_turn = False
		# Instance variable that tells the snake whether to turn left or right
		self.left_turn = None
		# If this is true, velocities will be drawn on the segments for debugging purposes
		self.draw_velocities = False

	def move(self):
		# Don't move if dead
		if not self.alive:
			return
		# Turn the head in the proper direction
		if self.should_turn:
			if self.left_turn:
				self.segments[0].turn_left()
			elif not self.left_turn:
				self.segments[0].turn_right()
			else:
				print("Error in Snake.move(): left_turn=None even though should_turn=True.")
		# Copy segments velocities so we can get previous values. Otherwise we would overwrite the data we need to read from
		old_velocities = []
		old_types = []
		for segment in self.segments:
			old_velocities.append(segment.velocity.copy())
			old_types.append(copy.copy(segment.type))

		for index, segment in enumerate(self.segments):
			# Handle head
			if index == 0:
				segment.move()
				continue
			# Handle second segment (for turns)
			if index == 1:
				if self.should_turn:
					if self.left_turn:
						segment.move(old_velocities[index - 1], SegmentTypes.BODY_LEFT)
					if not self.left_turn:
						segment.move(old_velocities[index - 1], SegmentTypes.BODY_RIGHT)
					continue
				else:
					segment.move(old_velocities[index], SegmentTypes.BODY_STRAIGHT)
				continue
			# Handle tail
			if index == len(self.segments)-1:
				segment.move(old_velocities[index-1])
				continue
			segment.move(old_velocities[index-1], old_types[index-1])
		# Reset turn variables for next move
		self.should_turn = False
		self.left_turn = None

	def turn(self):
		# If the player has already pressed space once, don't let them change the direction to a new random value
		if self.should_turn:
			return
		self.left_turn = random.choices([True, False])[0]
		self.should_turn = True

	def kill(self):
		self.alive = False

	def grow(self):
		pass

	# Initializes snake with proper length, starting at head_pos and moving with passed in velocity
	def set_snake_pos(self, head_tile=np.array([0, 0]), velocity=np.array([36, 0]), tile_size=16):
		self.segments = [Segment(SegmentTypes.HEAD, head_tile, velocity, tile_size, tile_size)]
		for x in range(self.length-1):
			new_type = SegmentTypes.BODY_STRAIGHT
			if x == self.length-2:
				new_type = SegmentTypes.TAIL
			# NOTE: This will not use velocity to decide which direction to spawn snake in
			new_tile = self.segments[x].tile - np.array([1, 0])
			new_seg = Segment(new_type, new_tile, velocity, tile_size, tile_size)
			self.segments.append(new_seg)

	# 		TODO: CHECK IF THIS GOES OFF THE BOARD!!!

	def draw(self, screen):
		for segment in self.segments:
			segment.draw(screen, self.draw_velocities)


