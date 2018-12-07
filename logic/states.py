from enum import Enum


# This class enumerates all the different states that the game can be in
class States(Enum):
	TITLE = 0
	GAME = 1
	SCORE = 2
	DEAD = 3
