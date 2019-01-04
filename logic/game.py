import numpy as np
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
	info_font = None
	board = Board((width, height))
	snake = Snake()
	difficulty = Difficulties(0)
	apple_spawn_rate = 2000  # milliseconds between apple spawns
	apple_spawn_amount = 1  # number of apples to spawn each time
	snake_speed = 500  # milliseconds between moves for snake
	SPAWN_APPLES = pg.USEREVENT+1
	MOVE = pg.USEREVENT+2
	start_time = 0
	score = 0

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
		self.font = pg.font.SysFont('Arial', 48, 1, 1)
		self.info_font = pg.font.SysFont('Arial', 18)

		# Init game logic
		self.state = States.TITLE
		# Set event timers
		pg.time.set_timer(self.SPAWN_APPLES, self.apple_spawn_rate)
		pg.time.set_timer(self.MOVE, self.snake_speed)
		# Loop until should_quit is changed to true
		while not self.should_quit:
			self.loop()
		return 0

	def loop(self):
		self.check_events()
		if self.state == States.GAME:
			if self.snake.alive:
				self.score = self.board.update_board(self.snake, self.score)
			else:
				self.state = States.DEAD
		self.draw()
		pg.display.update()

	def check_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.should_quit = True
			# Only spawn apples if event has been sent by timer and the player is in the game
			if event.type == self.SPAWN_APPLES and self.state == States.GAME:
				self.board.spawn_apples(self.apple_spawn_amount)
			# Only move at correct time intervals
			if event.type == self.MOVE:
				self.snake.move()
			# Check keypress
			if event.type == pg.KEYDOWN:
				# Quit on escape
				if event.key == pg.K_ESCAPE:
					self.should_quit = True
				# Handle button input
				if event.key == pg.K_SPACE:
					if self.state == States.GAME:
						self.snake.turn()
					elif self.state == States.TITLE:
						self.begin_game()
					elif self.state == States.DEAD:
						self.state = States.TITLE

	# Draw functions

	def draw(self):
		if self.state == States.TITLE:
			self.draw_title()
			self.draw_instructions()
		elif self.state == States.GAME:
			self.draw_game()
		elif self.state == States.SCORE:
			self.draw_score()
		elif self.state == States.DEAD:
			self.draw_dead()

	def draw_title(self):
		# TODO: Replace this with a picture logo Ethan made
		self.screen.fill([100, 100, 100])
		title_text = self.font.render('Stat-erpillar', True, (255, 255, 255))
		self.screen.blit(title_text, ((self.width/2) - title_text.get_rect().width/2, 10))

	def draw_instructions(self):
		instructions1 = "Instructions: "
		instructions2 = "Press the button to turn the snake. Collect as many apples as you can. "
		instructions3 = "Don't let the snake leave the board or run into itself"
		instructions4 = "Press to continue"
		instruction1_text = self.info_font.render(instructions1, True, (255, 255, 255))
		instruction2_text = self.info_font.render(instructions2, True, (255, 255, 255))
		instruction3_text = self.info_font.render(instructions3, True, (255, 255, 255))
		instruction4_text = self.info_font.render(instructions4, True, (255, 255, 255))
		self.screen.blit(instruction1_text, (
			(self.width / 2) - instruction1_text.get_rect().width / 2,
			(self.height / 2) - instruction1_text.get_rect().height / 2))
		self.screen.blit(instruction2_text, (
			(self.width / 2) - instruction2_text.get_rect().width / 2,
			(self.height / 2) - instruction2_text.get_rect().height / 2 + 50))
		self.screen.blit(instruction3_text, (
			(self.width / 2) - instruction3_text.get_rect().width / 2,
			(self.height / 2) - instruction3_text.get_rect().height / 2 + 100))
		self.screen.blit(instruction4_text, (
			(self.width / 2) - instruction4_text.get_rect().width / 2,
			(self.height / 2) - instruction4_text.get_rect().height / 2 + 150))

	def draw_game(self):
		self.screen.fill([0, 200, 0])
		self.board.draw(self.screen)
		self.snake.draw(self.screen)
		# Draw info box
		info_box = pg.Surface((200, 100))
		info_box.set_alpha(200)
		info_box.fill([255, 255, 255])
		self.screen.blit(info_box, (0, 0))
		# Draw info text
		time_text = self.info_font.render("Elapsed Time: " + str((pg.time.get_ticks()-self.start_time)/1000), True, (0, 0, 0))
		score_text = self.info_font.render("Score: " + str(self.score), True, (0, 0, 0))
		self.screen.blit(time_text, (5, 5))
		self.screen.blit(score_text, (5, 25))

	def draw_score(self):
		pass

	def draw_dead(self):
		white_box = pg.Rect(self.board.get_center()[0]-100, self.board.get_center()[1]-50, 200, 100)
		pg.draw.rect(self.screen, (255, 255, 255), white_box)
		title_text = self.font.render('You Died', True, (0, 0, 0))
		self.screen.blit(title_text, ((self.width / 2) - title_text.get_rect().width / 2, (self.height / 2) - title_text.get_rect().height / 2))

	def set_difficulty(self, difficulty):
		if difficulty == Difficulties.EASY:
			self.difficulty = difficulty.EASY
			self.apple_spawn_rate = 5000
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
		self.snake = Snake(4)
		self.snake.set_snake_pos(self.board.get_center_tile(), np.array([self.board.tile_size(), 0]), self.board.tile_size())
		self.board.clear()
		self.state = States.GAME
