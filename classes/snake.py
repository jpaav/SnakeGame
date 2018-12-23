import random

from classes.segment import Segment, SegmentTypes


class Snake:
	# Includes head and tail
	length = 3
	# X and Y component velocities stored as a tuple
	velocity = (1, 0)
	alive = True
	# Stores a list of tuples representing where the body currently is
	# Should have length matching length variable
	# First value should be head position, last value should be tail position
	segments = []

	def __init__(self, length=3, speed=250):
		self.length = length
		# TODO: Maybe remove this line from __init__?
		# idk its kinda essential and shouldn't be optional but gets called 3 times this way
		# self.set_snake_pos()

		# Number of milliseconds between moves
		self.speed = speed

		# Instance variable to detect whether the snake should turn next time it moves
		self.should_turn = False
		# Instance variable that tells the snake whether to turn left or right
		self.left_turn = None

	def move(self):
		# Don't move if dead
		self.should_turn = False
		self.left_turn = None

	def turn(self):
		# If the player has already pressed space once, don't let them change the direction to a new random value
		if self.should_turn:
			return
		self.left_turn = random.choices([True, False])
		print(self.left_turn)
		self.should_turn = True

	def kill(self):
		self.alive = False

	def grow(self):
		pass

	# Initializes snake with proper length, starting at head_pos and moving with passed in velocity
	def set_snake_pos(self, head_pos=(0, 0), velocity=(36, 0), tile_size=16):
		self.segments = [Segment(SegmentTypes.HEAD, head_pos, tile_size, tile_size)]
		for x in range(self.length-1):
			new_pos = Segment.subtract_tuples(self.segments[x].position, velocity)
			new_seg = Segment(SegmentTypes.BODY_STRAIGHT, new_pos, tile_size, tile_size)
			self.segments.append(new_seg)

	# 		TODO: CHECK IF THIS GOES OFF THE BOARD!!!

	def draw(self, screen):
		for segment in self.segments:
			segment.draw(screen)


