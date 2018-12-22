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
	body = []

	def __init__(self, length=3):
		self.length = length
		self.set_snake_pos()

	def move(self):
		# Don't move if dead
		pass

	def turn(self):
		# Do random decision for direction of turn here
		pass

	def kill(self):
		self.alive = False

	def grow(self):
		pass

	# Initializes snake with proper length, starting at head_pos and moving with passed in velocity
	def set_snake_pos(self, head_pos=(0, 0), velocity=(1, 0)):
		self.body = [Segment(head_pos, SegmentTypes.HEAD)]
		for x in range(self.length):
			self.body.append(Segment(Segment.subtract_tuples(self.body[x].position, velocity), SegmentTypes.BODY_STRAIGHT))
	# 		TODO: CHECK IF THIS GOES OFF THE BOARD!!!
		print(self.body)

	def draw(self):
		pass


