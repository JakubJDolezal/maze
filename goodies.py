'''
    goodies.py

    Definitions for some example goodies
'''

import random

from maze import Goody, UP, DOWN, LEFT, RIGHT, STAY, PING
#from maze import Goody
from baddies import RandomBaddy

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
        self.betweenPings=10
        self.xDir=False
        self.yDir=False
        self.badXDir=False
        self.badYDir=False
        self.oldPosX=1000
        self.oldPosY=1000
        self.RelXPos=0
        self.RelYPos=0
        self.randWalkerMode=0
        self.maxRandWalkerMode=10
        self.goodyPosition=0
        self.baddy_position=0

    def take_turn(self, obstruction, _ping_response):
#     ping every 10 turns and walk towards each other otherwise, if distance is same for long time walk randomly
        possibilities = [direction for direction in [UP, DOWN, LEFT, RIGHT] if not obstruction[direction]]
        Move=random.choice(possibilities)
        self.time=self.time+random.randint(0,1)
        if self.randWalkerMode>0:
            print("walk the walk")
            self.randWalkerMode=self.randWalkerMode-1
            if self.randWalkerMode==0:
                self.time=self.betweenPings
        else:
            self.get_player_relative_position(_ping_response)
            if isinstance( self.baddy_position, int)==False:
                print("Hey")
                print (abs(self.baddy_position.x+self.baddy_position.y))
                if (self.time>=self.betweenPings):
                    self.time=0
                    Move=PING
                    print("PINGUUUUU")
                print("Approach")   
                if (Move!=PING):
                    if (abs(self.baddy_position.x)+abs(self.baddy_position.y))<4 and abs(self.RelXPos)+abs(self.RelYPos)>2:
        #                FLEEEEEE
                        print(self.baddy_position.x+self.baddy_position.y)
                        print("Fleeee")
                        Move=self.flee(obstruction)
                        self.betweenPings=abs(self.baddy_position.x)+abs(self.baddy_position.y)-2
                    else:
                            Move=self.go_to_each_other(obstruction)
            else:
                if (self.time>=self.betweenPings):
                    self.time=0
                    Move=PING
                    print("PINGUUUUU")
                
                
        return Move
            
        

    def get_player_relative_position(self, _ping_response):
#    	''' extracts where the other player is from the _ping_response input using is instance to
#    	distinguish between goodie and baddie'''
        if _ping_response is not None:
            print("Analysis")
            self.time=0
            for player, position in _ping_response.items():
                if isinstance(player, Goody):
                    if isinstance( self.goodyPosition, int )==False:
                        self.oldPosX=self.goodyPosition.x
                        self.oldPosY=self.goodyPosition.y
                    self.goodyPosition = position
                    self.RelXPos=position.x
                    self.RelYPos=position.y
                    self.betweenPings=abs(self.RelXPos)+abs(self.RelYPos)
                    if self.oldPosX>=self.goodyPosition.x and self.oldPosX>=self.goodyPosition.y:
                        self.randWalkerMode=self.maxRandWalkerMode
                        print("Random Mode Activated")
                        self.maxRandWalkerMode=self.maxRandWalkerMode+5
                else:
                    self.baddy_position = position                  
                    
        if isinstance( self.goodyPosition, int )==False:
            if self.RelXPos>0:
                self.xDir=True
            else:
                self.xDir=False
            if  self.RelYPos>0:
                self.yDir=True
            else:
                self.yDir=False
                
        if isinstance( self.baddy_position, int )==False:
            if self.baddy_position.x>0:
                self.badXDir=True
            else:
                self.badXDir=False
            if self.baddy_position.y>0:
                self.badYDir=True
            else:
                self.badYDir=False
    
    
    def go_to_each_other(self, obstruction): 
        possibilities = [direction for direction in [UP, DOWN, LEFT, RIGHT] if not obstruction[direction]]
        Move=random.choice(possibilities)
        towards=False
        count=0
        while towards==False:
            decision=random.random();
            if decision>abs(self.RelXPos)/(abs(self.RelXPos)+abs(self.RelYPos)):
                if self.xDir==True and obstruction[RIGHT]==False:
                    Move=RIGHT
                    print("Right")
                    self.RelXPos=self.RelXPos-1
                    break
                else:
                    if obstruction[LEFT]==False:
                        Move=LEFT
                        print("LEft")
                        self.RelXPos=self.RelXPos+1
                        break
            else:
                if self.yDir==True and obstruction[UP]==False:
                    Move=UP
                    self.RelYPos=self.RelYPos-1
                    print("UP")
                    break
                else:
                    if obstruction[DOWN]==False:
                        Move=DOWN
                        self.RelYPos=self.RelYPos+1
                        print("DOWN")
                        break
            count=count+1
            if (count>6):
                break
        
        return Move

    def flee(self,obstruction):
        possibilities = [direction for direction in [UP, DOWN, LEFT, RIGHT] if not obstruction[direction]]
        Move=random.choice(possibilities)
        towards=False
        count=0
        while towards==False:
            decision=random.random();
            if decision>abs(self.baddy_position.x)/(abs(self.baddy_position.x)+abs(self.baddy_position.y)+1):
                if self.badXDir==False and obstruction[RIGHT]==False:
                    Move=RIGHT
                    self.RelXPos=self.RelXPos+1
                    break
                else:
                    if obstruction[LEFT]==False:
                        Move=LEFT
                        self.RelXPos=self.RelXPos-1
                        break
            else:
                if self.badYDir==True and obstruction[UP]==False:
                    Move=DOWN
                    self.RelYPos=self.RelYPos+1
                    break
                else:
                    if obstruction[DOWN]==False:
                        Move=UP
                        self.RelYPos=self.RelYPos-1
                        break
            count=count+1
            if count>6:
                break
        return Move
