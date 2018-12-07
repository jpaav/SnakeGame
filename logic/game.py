import pygame as pg

from logic.states import States


class SnakeGame:
	should_quit = False
	height = 600
	width = 600
	state = States(0)
	screen = pg.display.set_mode((width, height))
	font = None

	def start(self):
		# Init PyGame
		(passed, failed) = pg.init()
		print("Number of modules successfully loaded: " + str(passed))
		print("Number of modules failed to load: " + str(failed))
		# Close program if any modules fail to load
		if failed > 0:
			return 1
		# Create screen with given dimensions
		pg.display.set_mode((self.width, self.height))
		pg.display.set_caption("Staterpillar")
		self.font = pg.font.SysFont('Comic Sans MS', 30)
		# Init game logic
		self.state = States.TITLE

		# Loop until should_quit is changed to true
		while not self.should_quit:
			self.loop()
		return 0

	def loop(self):
		self.get_keyboard_input()
		self.check_quit()
		self.draw()
		pg.display.update()

	def check_quit(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.should_quit = True

	def get_keyboard_input(self):
		keys_pressed = pg.key.get_pressed()
		if keys_pressed[pg.K_ESCAPE]:
			self.should_quit = True
		return

	# Draw functions

	def draw(self):
		if self.state == States.TITLE:
			self.draw_title()
		elif self.state == States.GAME:
			self.draw_game()
		elif self.state == States.SCORE:
			self.draw_score()
		elif self.state == States.DEAD:
			self.draw_dead()

	def draw_title(self):
		# TODO: Replace this with a picture logo Ethan made
		self.screen.fill([0, 200, 0])
		title_text = self.font.render('Staterpillar', True, (255, 255, 255))
		self.screen.blit(title_text, ((self.width/2) - title_text.get_rect().width/2, 10))

	def draw_game(self):
		pass

	def draw_score(self):
		pass

	def draw_dead(self):
		pass
