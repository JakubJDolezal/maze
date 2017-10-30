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

    def __init__(self):
        self.time=0
        self.betweenPings=10
        self.x_dir=False
        self.y_dir=False
        self.lastPing=0

    def take_turn(self, obstruction, _ping_response):
#     ping every 10 turns and walk towards each other
        possibilities = [direction for direction in [UP, DOWN, LEFT, RIGHT] if not obstruction[direction]]
        Move=random.choice(possibilities)
        self.time=self.time+1
        if (self.time>=self.betweenPings):
            self.time=0
            Move=PING
        else:
            if _ping_response is not None:
                for player, position in _ping_response.items():
                    if isinstance(player, Goody):
                        self.goody_position = position
                    else:
                        self.baddy_position = position
                if abs( self.goody_position.x)>0:
                    self.x_dir=True
                else:
                    self.x_dir=False
                if abs( self.goody_position.y>0):
                    self.y_dir=True
                else:
                    self.y_dir=False           
            decision=random.randint(0, 1)
            if decision==1:
                if self.x_dir==True and obstruction[LEFT]==False:
                    Move=LEFT
                else:
                    if obstruction[RIGHT]==False:
                        Move=RIGHT
            else:
                if self.y_dir==True and obstruction[UP]==False:
                    Move=UP
                else:
                    if obstruction[DOWN]==False:
                        Move=DOWN
            
            
        return Move
            
        

#    def get_player_relative_position(self, _ping_response):
#    	''' extracts where the other player is from the _ping_response input using is instance to
#    	distinguish between goodie and baddie'''
#    	pass
#	

