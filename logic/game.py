import pygame as pg

from classes.board import Board
from classes.snake import Snake
from logic.difficulties import Difficulties
from logic.states import States


class SnakeGame:
	should_quit = False
	height = 600
	width = 600
	state = States(0)
	screen = pg.display.set_mode((width, height))
	font = None
	board = Board()
	snake = Snake()
	difficulty = Difficulties(0)
	apple_spawn_rate = 2000  # milliseconds between apple spawns
	apple_spawn_amount = 1  # number of apples to spawn each time
	SPAWN_APPLES = pg.USEREVENT+1
	start_time = 0

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
		# Set event timers
		pg.time.set_timer(self.SPAWN_APPLES, self.apple_spawn_rate)
		# Loop until should_quit is changed to true
		while not self.should_quit:
			self.loop()
		return 0

	def loop(self):
		self.check_events()
		self.snake.move()
		collision = self.board.update_board(self.snake)
		if collision:
			self.kill_snake()
		self.draw()
		pg.display.update()

	def check_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.should_quit = True
			if event.type == self.SPAWN_APPLES:
				self.board.spawn_apples(self.apple_spawn_amount)
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.should_quit = True
				if event.key == pg.K_SPACE:
					self.snake.turn()

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

	def set_difficulty(self, difficulty):
		if difficulty == Difficulties.EASY:
			self.difficulty = difficulty.EASY
			self.apple_spawn_rate = 2000
			self.apple_spawn_amount = 1
		if difficulty == Difficulties.MEDIUM:
			self.difficulty = difficulty.MEDIUM
			self.apple_spawn_rate = 1000
			self.apple_spawn_amount = 2
		if difficulty == Difficulties.HARD:
			self.difficulty = difficulty.HARD
			self.apple_spawn_rate = 500
			self.apple_spawn_amount = 3

	def begin_game(self):
		self.start_time = pg.time.get_ticks()
		self.snake = Snake()
		self.state = States.GAME

	def kill_snake(self):
		self.snake.kill()
		self.state = States.DEAD
