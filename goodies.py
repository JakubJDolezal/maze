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
        self.oldPosX=5
        self.oldPosY=5
        self.RelXPos=0
        self.RelYPos=0
        self.randWalkerMode=0
        self.nonRandWalkerMode=10
        self.maxRandWalkerMode=5
        self.goodyPosition=0
        self.baddy_position=0
        w, h = 50, 50;
        self.madeMap = [[1 for x in range(w)] for y in range(h)]
        self.mapHunting=[[10 for x in range(w)] for y in range(h)]
        self.possibilities=0
        self.mapPosition=[20,20]
        self.foundHim=False
        self.maxDis=-1000
        self.reached=False

    def take_turn(self, obstruction, _ping_response):
#     ping every 10 turns and walk towards each other otherwise, if distance is same for long time walk randomly
        self.get_player_relative_position(_ping_response)
        self.time=self.time+random.randint(0,1)
        
        if self.foundHim==False:
            self.nonRandWalkerMode=self.nonRandWalkerMode-1
            self.mapMaking(obstruction)
            Move=random.choice(self.possibilities)
            
            if self.randWalkerMode>0 and self.nonRandWalkerMode<0:
               self.random_walker_mode() 
            else:
                if isinstance( self.baddy_position, int)==False:
                    print (abs(self.baddy_position.x+self.baddy_position.y))
                    if (self.time>self.betweenPings):
                        self.time=0
                        Move=PING  
                    if (Move!=PING):
                        if (abs(self.baddy_position.x)+abs(self.baddy_position.y))<5 and abs(self.RelXPos)+abs(self.RelYPos)>2:
                            Move=self.flee(obstruction)
                            self.betweenPings=abs(self.baddy_position.x)+abs(self.baddy_position.y)-2
                        else:
                            Move=self.go_to_each_other(obstruction)
                else:
                    if (self.time>=self.betweenPings):
                        self.time=0
                        Move=PING
            if self.madeMap[self.mapPosition[0]][self.mapPosition[1]]>15 and self.madeMap[self.mapPosition[0]][self.mapPosition[1]]<50  and Move!=PING:
                Move=self.moveAlongWall(obstruction)
            if self.madeMap[self.mapPosition[0]][self.mapPosition[1]]>50:
                self.randWalkerMode=self.maxRandWalkerMode
                
        else:
            Move=self.foundPath()
            
        self.updatePosition(Move)        
       
        return Move
   
    def random_walker_mode(self):
        self.randWalkerMode=self.randWalkerMode-1
        self.nonRandWalkerMode=self.nonRandWalkerMode+1
        if self.randWalkerMode==0:
            self.time=self.betweenPings
            self.nonRandWalkerMode=self.maxRandWalkerMode  
        pass
            

    def get_player_relative_position(self, _ping_response):
#    	''' extracts where the other player is from the _ping_response input using is instance to
#    	distinguish between goodie and baddie'''
        if _ping_response is not None:
            self.time=0
            for player, position in _ping_response.items():
                if isinstance(player, Goody):
                    if isinstance( self.goodyPosition, int )==False:
                        self.oldPosX=round(self.goodyPosition.x)
                        self.oldPosY=round(self.goodyPosition.y)
                    self.goodyPosition = position
                    self.RelXPos=position.x
                    self.RelYPos=position.y
                    self.betweenPings=max(abs(self.RelXPos)+abs(self.RelYPos),5)
                    if abs(self.oldPosX)+abs(self.oldPosY)>=abs(self.goodyPosition.x)+abs(self.goodyPosition.y):
                        self.randWalkerMode=self.maxRandWalkerMode
                        self.maxRandWalkerMode=self.maxRandWalkerMode+5
                        self.nonRandWalkerMode=0
                else:
                    self.baddy_position = position
            if self.madeMap[self.mapPosition[0]+self.RelXPos][self.mapPosition[1]+self.RelYPos]!=1:
                self.foundHim=True
                self.foundYou()
                    
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
        Move=random.choice(self.possibilities)
        towards=False
        count=0
        while towards==False:
            decision=random.random();
            if decision>abs(self.RelXPos)/(abs(self.RelXPos)+abs(self.RelYPos)+1):
                if self.xDir==True and RIGHT in self.possibilities:
                    Move=RIGHT
                    break
                else:
                    if LEFT in self.possibilities:
                        Move=LEFT
                        break
            else:
                if self.yDir==True and UP in self.possibilities:
                    Move=UP                    
                    break
                else:
                    if DOWN in self.possibilities:
                        Move=DOWN
                        break
            count=count+1
            if (count>6):
                break
        
        return Move

    def flee(self,obstruction):
        Move=random.choice(self.possibilities)
        towards=False
        count=0
        while towards==False:
            decision=random.random();
            if decision>abs(self.baddy_position.x)/(abs(self.baddy_position.x)+abs(self.baddy_position.y)+1):
                if self.badXDir==False and RIGHT in self.possibilities:
                    Move=RIGHT
                    break
                else:
                    if LEFT in self.possibilities:
                        Move=LEFT
                        break
            else:
                if self.badYDir==True and DOWN in self.possibilities:
                    Move=DOWN
                    break
                else:
                    if UP in self.possibilities:
                        Move=UP
                        break
            count=count+1
            if count>6:
                break
        return Move
    
    def mapMaking(self, obstruction):
        surrounded=0
        self.BeenLeft=self.madeMap[self.mapPosition[0]][self.mapPosition[1]-1]
        self.BeenRight=self.madeMap[self.mapPosition[0]][self.mapPosition[1]+1]
        self.BeenUp=self.madeMap[self.mapPosition[0]+1][self.mapPosition[1]]
        self.BeenDown=self.madeMap[self.mapPosition[0]-1][self.mapPosition[1]]
        
        if obstruction[UP]==True or self.BeenRight==0:
            self.madeMap[self.mapPosition[0]][self.mapPosition[1]+1]=0
            surrounded=surrounded+1
        if obstruction[DOWN]==True or self.BeenLeft==0:
            self.madeMap[self.mapPosition[0]][self.mapPosition[1]-1]=0
            surrounded=surrounded+1
        if obstruction[RIGHT]==True or self.BeenUp==0:
            self.madeMap[self.mapPosition[0]+1][self.mapPosition[1]]=0
            surrounded=surrounded+1
        if obstruction[LEFT]==True or self.BeenDown==0:
            self.madeMap[self.mapPosition[0]-1][self.mapPosition[1]]=0
            surrounded=surrounded+1
            
        if surrounded==3:
            self.madeMap[self.mapPosition[0]][self.mapPosition[1]]=0
                        
        if self.madeMap[self.mapPosition[0]][self.mapPosition[1]]!=0:
            print(self.madeMap[self.mapPosition[0]][self.mapPosition[1]])
            self.madeMap[self.mapPosition[0]][self.mapPosition[1]]=self.madeMap[self.mapPosition[0]][self.mapPosition[1]]+1
                        
        self.possibilities = [direction for direction in [UP, DOWN, LEFT, RIGHT]]
        if self.madeMap[self.mapPosition[0]][self.mapPosition[1]+1]==0:
            self.possibilities.remove(UP)
        if self.madeMap[self.mapPosition[0]][self.mapPosition[1]-1]==0:
            self.possibilities.remove(DOWN)
        if self.madeMap[self.mapPosition[0]+1][self.mapPosition[1]]==0:
            self.possibilities.remove(RIGHT)
        if self.madeMap[self.mapPosition[0]-1][self.mapPosition[1]]==0:
            self.possibilities.remove(LEFT)
        
        
     
    def moveAlongWall(self, obstruction):
        Move=random.choice(self.possibilities)
        sum=(self.BeenDown+self.BeenUp+self.BeenRight+self.BeenLeft)   
        decision=random.random()*sum
        if decision<(sum-2*self.BeenRight-abs(self.RelXPos)) and obstruction[RIGHT]==False:
             Move=RIGHT
        else:
            if decision<(sum-2*self.BeenLeft+abs(self.RelXPos)) and obstruction[LEFT]==False:
                Move=LEFT
            else:
                if decision<(sum-2*self.BeenUp-abs(self.RelYPos)) and obstruction[UP]==False:
                    Move=UP
                else:
                    if decision<(sum-2*self.BeenDown+abs(self.RelYPos)) and obstruction[DOWN]==False:
                        Move=DOWN
        return Move
        
    def updatePosition(self,Move):
#        
        if Move==RIGHT:
            self.mapPosition[0]=self.mapPosition[0]+1
            self.RelXPos=self.RelXPos+1
        if Move==LEFT:
            self.RelXPos=self.RelXPos-1
            self.mapPosition[0]=self.mapPosition[0]-1
        if Move==UP:
            self.RelYPos=self.RelYPos+1
            self.mapPosition[1]=self.mapPosition[1]+1
        if Move==DOWN:
            self.mapPosition[1]=self.mapPosition[1]-1
            self.RelYPos=self.RelYPos-1

    def foundYou(self):
        self.mapHunting=[[10 for x in range(50)] for y in range(50)]
        self.recursivePathing(self.mapPosition[0]+self.RelXPos, self.mapPosition[1]+self.RelYPos, -1,0,0)
        pass                  
        
    def recursivePathing(self, i, j, number, l, k): 
#        Recursively creates path
        if number<self.maxDis:
            pass
        if (self.madeMap[i][j]!=0 and self.madeMap[i][j]!=1) and ((self.mapHunting[i][j]<number or self.mapHunting[i][j]==10) or (self.mapHunting[i][j]>0)):
            self.mapHunting[i][j]=number
            if i==self.mapPosition[0] and j==self.mapPosition[1]:
                self.maxDis=number
                pass
            i1=1
            if i1!=l:
                self.recursivePathing(i+i1,j, number-1,-i1,0)
            i1=-1
            if i1!=l:
                self.recursivePathing(i+i1,j, number-1,-i1,0)
            j1=1
            if j1!=k:
                self.recursivePathing(i,j+j1, number-1,0, -j1)
            j1=-1
            if j1!=k:
                self.recursivePathing(i,j+j1, number-1,0, -j1)
                    
    def foundPath(self):
        Move=None
        print(self.mapHunting)
        if self.mapHunting[self.mapPosition[0]][self.mapPosition[1]+1]==(self.mapHunting[self.mapPosition[0]][self.mapPosition[1]]+1):
            Move=UP
        if self.mapHunting[self.mapPosition[0]][self.mapPosition[1]-1]==(self.mapHunting[self.mapPosition[0]][self.mapPosition[1]]+1):
            Move=DOWN
        if self.mapHunting[self.mapPosition[0]+1][self.mapPosition[1]]==(self.mapHunting[self.mapPosition[0]][self.mapPosition[1]]+1):
            Move=RIGHT
        if self.mapHunting[self.mapPosition[0]-1][self.mapPosition[1]]==(self.mapHunting[self.mapPosition[0]][self.mapPosition[1]]+1):
            Move=LEFT
        if self.mapHunting[self.mapPosition[0]][self.mapPosition[1]]==-1 or self.reached==True:
            Move=PING
            self.reached=True
            self.foundHim=False
        return Move
        