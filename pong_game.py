import pygame
import numpy as np
import time

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

PLAYER_MOVEMENT_SPEED = 700  # screen widths per second
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 20

TOP_PLAYER_Y_POS = 10
BOTTOM_PLAYER_Y_POS = SCREEN_HEIGHT - TOP_PLAYER_Y_POS - PLAYER_HEIGHT

CURVE_FACTOR = 7.0

BACKGROUND_COLOUR = (255, 255, 255)


class Ball:
	def __init__(self, size):
		self.size = size
		self.colour = (0, 0, 255)
		self.thickness = 1
		
		self.r = np.array([300.0, 300.0])  # position
		self.V = np.array([0.0, 300.0])  # velocity
	
	def restart(self):
		self.r = np.array([300.0, 300.0])
	
	def step(self, dT, game):
		self.r += self.V * dT
	
		# right and left bounces
		if self.r[0] + self.size > SCREEN_WIDTH:
			self.r[0] = 2 * SCREEN_WIDTH - 2 * self.size - self.r[0]
			self.V[0] = -self.V[0]
		elif self.r[0] - self.size < 0:
			self.r[0] = 2 * self.size - self.r[0]
			self.V[0] = -self.V[0]
		
		# player bounces
		if self.r[1] + self.size > BOTTOM_PLAYER_Y_POS:
			if game.bottom_player.position <= self.r[0] <= game.bottom_player.position + PLAYER_WIDTH:
				self.r[1] = 2 * BOTTOM_PLAYER_Y_POS - 2 * self.size - self.r[1]
				self.V[1] = -self.V[1]
				self.V[0] = self.V[0] + CURVE_FACTOR * (self.r[0] - (game.bottom_player.position + PLAYER_WIDTH / 2))
			else:
				# print('bottom player is a loser')
				game.winner = game.top_player
		elif self.r[1] - self.size < TOP_PLAYER_Y_POS + PLAYER_HEIGHT:
			if game.top_player.position <= self.r[0] <= game.top_player.position + PLAYER_WIDTH:
				self.r[1] = 2 * (TOP_PLAYER_Y_POS + PLAYER_HEIGHT) + 2 * self.size - self.r[1]
				self.V[1] = -self.V[1]
				self.V[0] = self.V[0] + CURVE_FACTOR * (self.r[0] - (game.top_player.position + PLAYER_WIDTH/2))
			else:
				# print('top player is a loser')
				game.winner = game.bottom_player
	
	def draw(self):
		pygame.draw.circle(screen, self.colour, (int(self.r[0]), int(self.r[1])), self.size, self.thickness)


class Player:
	def __init__(self, colour):
		self.colour = colour
		self.yPos = 0  # N.B. remember to initialise this properly
		self.position = 300
		self.movement = 0  # -1 for left, 0 for stay still, 1 for right
	
	def step(self, dT):
		self.position = min(max(self.position + self.movement * PLAYER_MOVEMENT_SPEED * dT, 0),
		                    SCREEN_WIDTH - PLAYER_WIDTH)  # don't let them move off the end of the screen
	
	def ai_move(self, position, opponent_position, ball_r, ball_v):
		pass
	
	def draw(self):
		pygame.draw.rect(screen, self.colour, (self.position, self.yPos, PLAYER_WIDTH, PLAYER_HEIGHT))


class Game:
	def __init__(self, top_player, bottom_player):
		self.top_player = top_player
		self.bottom_player = bottom_player
		self.ball = Ball(10)
		
		self.top_player.yPos = TOP_PLAYER_Y_POS
		self.bottom_player.yPos = BOTTOM_PLAYER_Y_POS
		
		self.winner = None

	def step(self, dT):
		
		# centres of players divided by SCREEN_WIDTH to "normalise" between 0 and 1 (sort of)
		top = (self.top_player.position + PLAYER_WIDTH/2) / SCREEN_WIDTH
		bottom = (self.bottom_player.position + PLAYER_WIDTH/2) / SCREEN_WIDTH
		r = self.ball.r.copy()
		V = self.ball.V.copy()
		
		# also "normalise" ball position and velocity
		self.top_player.ai_move(top, bottom, r/SCREEN_WIDTH, V/SCREEN_WIDTH)
		
		# reflect the game for the bottom player so it looks as if it were the top player
		r[1] = SCREEN_HEIGHT - r[1]
		V[1] = - V[1]
		
		self.bottom_player.ai_move(bottom, top, r/SCREEN_WIDTH, V/SCREEN_WIDTH)
		
		self.bottom_player.step(dT)
		self.top_player.step(dT)
		self.ball.step(dT, self)
	
	def draw(self, screen):
		screen.fill(BACKGROUND_COLOUR)
		self.top_player.draw()
		self.bottom_player.draw()
		self.ball.draw()
	
	def restart(self):
		self.ball.restart()
		self.winner = None


def play_against(top_player):
	bottom_player = Player((0, 0, 255))
	game = Game(top_player=top_player, bottom_player=bottom_player)
	
	global screen
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('Pong')
	
	previous_time = time.time()
	running = True
	while running:
		current_time = time.time()
		dT = current_time - previous_time
		previous_time = current_time
		
		game.step(dT)
		game.draw(screen)
		
		pygame.display.flip()
		
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					bottom_player.movement -= 1
				elif event.key == pygame.K_RIGHT:
					bottom_player.movement += 1
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					bottom_player.movement += 1
				elif event.key == pygame.K_RIGHT:
					bottom_player.movement -= 1
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					top_player.movement -= 1
				elif event.key == pygame.K_d:
					top_player.movement += 1
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_a:
					top_player.movement += 1
				elif event.key == pygame.K_d:
					top_player.movement -= 1
			
			elif event.type == pygame.QUIT:
				running = False


if __name__ == '__main__':
	play_against(Player((255, 0, 0)))