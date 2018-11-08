import pong_game as pg
import numpy as np
import random


class NNPlayer(pg.Player):
	
	def __init__(self, colour):
		super().__init__(colour)
		self.wins = 0
		self.W1 = np.random.randn(6)
		self.b1 = random.normalvariate(0, 1)
	
	def ai_move(self, position, opponent_position, ball_r, ball_v):  # gets called on each step
		x = np.hstack((position, opponent_position, ball_r, ball_v))
		y = np.dot(self.W1, x) + self.b1
		
		if y < -0.3:
			self.movement = -1  # go left
		elif y > 0.3:
			self.movement = 1  # go right
		else:
			self.movement = 0  # stay still
	
	def mutate(self):
		mutation_index = np.random.choice(self.W1.shape[0], 1)  # choose a weight to mutate
		self.W1[mutation_index] += random.normalvariate(0, 0.2)
		self.b1 += random.normalvariate(0, 0.05)
	
	def clone(self):
		clone = NNPlayer(self.colour)
		clone.W1 = self.W1.copy()
		clone.b1 = self.b1
		return clone


players = []
for i in range(200):
	players.append(NNPlayer((0, 255, 0)))

for i in range(30000):
	if i % 100 == 0:  # progress indicator
		print(i)
	
	tributes = np.random.choice(200, 2, replace=False)  # choose 2 tributes
	top_player = players[tributes[0]]
	bottom_player = players[tributes[1]]
	game = pg.Game(top_player=top_player, bottom_player=bottom_player)  # ONLY ONE WILL SURVIVE THE HUNGER GAMES!
	
	while not game.winner:  # IT ONLY ENDS WHEN ONE DIES!!!
		game.step(0.1)  # run the game 0.1 seconds per step
	
	# A clone of the winner takes the losers place
	# The winner also gets mutated a bit
	# Now there are 2 copies of the winner (one mutated and one not)
	if game.winner == top_player:
		players[tributes[1]] = top_player.clone()
		top_player.mutate()
		top_player.wins += 1
	else:
		players[tributes[0]] = bottom_player.clone()
		bottom_player.mutate()
		bottom_player.wins += 1

# find the one that's currently winning the most and play against it!
index = 0
for i in range(200):
	if players[i].wins > players[index].wins:
		index = i

pg.play_against(players[index])
