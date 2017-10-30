'''
    goodies.py

    Definitions for some example goodies
'''

import random

from maze import Goody, UP, DOWN, LEFT, RIGHT, STAY, PING

class StaticGoody(Goody):
    ''' A static goody - does not move from its initial position '''

    def take_turn(self, _obstruction, _ping_response):
        ''' Stay where we are '''
        return STAY

class RandomGoody(Goody):
    ''' A random-walking goody '''

    def take_turn(self, obstruction, _ping_response):
        ''' Ignore any ping information, just choose a random direction to walk in, or ping '''
        possibilities = [direction for direction in [UP, DOWN, LEFT, RIGHT] if not obstruction[direction]] + [PING]
        return random.choice(possibilities)

class BiasedGoody(Goody):
    ''' A goody that is biased to walk towards one another '''

    def take_turn(self, obstruction, _ping_response):
        ''' ping every 10 turns and walk towards each other '''
        pass

    def player_bias(self, _ping_response):
	''' decides which direction to move towards based on where the other player is'''
	pass

    def get_player_relative_position(self, _ping_response):
	''' extracts where the other player is from the _ping_response input using isinstance to
	distinguish between goodie and baddie'''
	pass
	

