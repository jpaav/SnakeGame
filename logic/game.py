import pygame as pg

from logic.states import States


class SnakeGame:
	should_quit = False
	height = 600
	width = 600
	screen = States()

	def start(self):
		#
		# Init PyGame
		#
		(passed, failed) = pg.init()
		print("Number of modules successfully loaded: " + str(passed))
		print("Number of modules failed to load: " + str(failed))
		# Close program if any modules fail to load
		if failed > 0:
			return 1
		# Create screen with given dimensions
		pg.display.set_mode((self.width, self.height))
		#
		# Init game logic
		#
		self.screen = States.TITLE
		# Loop until should_quit is changed to true
		while not self.should_quit:
			self.loop()
		return 0

	def loop(self):
		self.get_keyboard_input()
		self.check_quit()
		pg.display.flip()

	def check_quit(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.should_quit = True

	def get_keyboard_input(self):
		keys_pressed = pg.key.get_pressed()
		if keys_pressed[pg.K_ESCAPE]:
			self.should_quit = True
		return




