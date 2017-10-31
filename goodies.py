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
        self.time=9
        self.betweenPings=5
        self.x_dir=False
        self.y_dir=False
        self.lastPing=0
        self.randWalkerMode=0
        self.maxRandWalkerMode=10
        self.goodyPosition=0

    def take_turn(self, obstruction, _ping_response):
#     ping every 10 turns and walk towards each other otherwise, if distance is same for long time walk randomly
        possibilities = [direction for direction in [UP, DOWN, LEFT, RIGHT] if not obstruction[direction]]
        Move=random.choice(possibilities)      
        if self.randWalkerMode>0:
            self.randWalkerMode=self.randWalkerMode-1
            print("Random Mode")
        else:
            if _ping_response is not None:
                self.get_player_relative_position(_ping_response)
                self.time=0
            self.time=self.time+random.randint(0,1)
            if (self.time>=self.betweenPings):
                self.time=0
                Move=PING
                print("PINGUUUUU")
            else:
                     
                decision=random.randint(0, 1)
                if decision==1:
                    if self.x_dir==True and obstruction[RIGHT]==False:
                        Move=RIGHT
                    else:
                        if obstruction[LEFT]==False:
                            Move=LEFT
                else:
                    if self.y_dir==True and obstruction[UP]==False:
                        Move=UP
                    else:
                        if obstruction[DOWN]==False:
                            Move=DOWN
                
                
        return Move
            
        

    def get_player_relative_position(self, _ping_response):
#    	''' extracts where the other player is from the _ping_response input using is instance to
#    	distinguish between goodie and baddie'''
        for player, position in _ping_response.items():
            if isinstance(player, Goody):
                self.oldPos=self.goodyPosition
                self.goodyPosition = position
                if self.oldPos==self.goodyPosition:
                    self.randWalkerMode=self.maxRandWalkerMode
                    print("Random Mode Activated")
                    self.maxRandWalkerMode=self.maxRandWalkerMode+5
            else:
                self.baddy_position = position
        if abs( self.goodyPosition.x)>0:
            self.x_dir=True
        else:
            self.x_dir=False
        if abs( self.goodyPosition.y>0):
            self.y_dir=True
        else:
            self.y_dir=False      
	

