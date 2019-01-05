import datetime

import numpy as np
import pygame as pg
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from uuid import getnode

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
	snake_speed = 1000  # milliseconds between moves for snake
	SPAWN_APPLES = pg.USEREVENT+1
	MOVE = pg.USEREVENT+2
	start_time = 0
	score = 0
	should_upload_scores = True

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
				# Upload score
				if self.should_upload_scores:
					self.upload_score()
				# Go to dead state
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
		elif self.state == States.GAME:
			self.draw_game()
		elif self.state == States.SCORE:
			self.draw_score()
		elif self.state == States.DEAD:
			self.draw_dead()

	def draw_title(self):
		# TODO: Replace this with a picture logo Ethan made
		self.screen.fill([0, 200, 0])
		title_text = self.font.render('Stat-erpillar', True, (255, 255, 255))
		self.screen.blit(title_text, ((self.width/2) - title_text.get_rect().width/2, 10))

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
		self.snake = Snake(4)
		self.snake.set_snake_pos(self.board.get_center_tile(), np.array([self.board.tile_size(), 0]), self.board.tile_size())
		self.board.clear()
		self.score = 0
		self.state = States.GAME

	def upload_score(self):
		SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
		store = file.Storage('token.json')
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
			creds = tools.run_flow(flow, store)
		service = build('sheets', 'v4', http=creds.authorize(Http()))

		# Call the Sheets API
		sheet = service.spreadsheets()
		dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		new_entry = [
			[
				dt, self.score, getnode(), pg.time.get_ticks() - self.start_time
			]
		]
		body = {
			'values': new_entry
		}
		result = sheet.values().append(
			spreadsheetId='1vxIHPnCOS1Uv42N-aKQwkB3daFM-0W23-A_It9vYEPw', range='Uploaded_Data!A1:D1',
			valueInputOption="USER_ENTERED", body=body).execute()
		print('{0} cells appended .'.format(result.get('updates').get('updatedCells')))

