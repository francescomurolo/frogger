from random import choice, randrange
from actor import Actor, Arena
from raft import Raft
from river import River
from turtle import Turtle
from crocodile import Crocodile

class Vehicle(Actor):
    def __init__(self, arena, x, y, dim):
        self._type=0
        self._dim=dim
        self._x, self._y = x, y
        if self._dim==1:
            self._w, self._h = 50, 20
            self._speed = 2
            self._type=0
        elif self._dim==2:
            self._w, self._h = 33, 22
            self._speed = 2
            self._type=1
        elif self._dim==3:
            self._w, self._h = 30, 20
            self._speed = 1
            self._type=0
        elif self._dim==4:
            self._w, self._h = 35, 25
            self._speed = 2
            self._type=1
        elif self._dim==5:
            self._w, self._h = 30, 25
            self._speed = 3
            self._type=0
            
        self._dx, self._dy = self._speed, self._speed
        self._arena = arena
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        if self._type==0:
            self._x -= self._dx
            if self._x < -self._w:
                self._x=(arena_w+arena_w/100*40)-self._w
        elif self._type==1:
            self._x += self._dx
            if self._x > arena_w+self._w:
                self._x=(-arena_w/100*40)+self._w
            
    def collide(self, other):
        pass
    
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        if self._dim==1:
            return 102, 300, self._w, self._h
        elif self._dim==2:
            return 72, 300, self._w, self._h
        elif self._dim==3:
            return 7, 268, self._w, self._h
        elif self._dim==4:
            return 38, 265, self._w, self._h
        elif self._dim==5:
            return 81, 265, self._w, self._h

class Frog(Actor):
    def __init__(self, arena, x, y):
        self._x_start, self._y_start = x, y
        self._x, self._y = x, y
        self._w, self._h = 20,19
        self._speed = 3
        self._dead = 0
        self._score = 0
        self._dx, self._dy = 0, 0
        self._arena = arena
        self._collideRaft=False
        self._collideTurtle=False
        self._collideRiver=False
        self._collideCrocodile=False
        self._win=False
        self._bonus=False
        self._areas = [False, False, False, False, False]
        arena.add(self)
        
    def move(self):
        arena_w, arena_h = self._arena.size()
        self._y += self._dy
        if self._y < 54:
            self._y = 54
        elif self._y > arena_h - 42:
            self._y = arena_h - 42

        self._x += self._dx
        if self._x < 0:
            self._x = 0
        elif self._x > arena_w - self._w:
            self._x = arena_w - self._w

    def go_left(self):
        self._dx, self._dy = -self._speed, 0
        
    def go_right(self):
        self._dx, self._dy = +self._speed, 0

    def go_up(self):
        self._dx, self._dy = 0, -self._speed
        
    def go_down(self):
        self._dx, self._dy = 0, +self._speed
    
    def stay(self):
        self._dx, self._dy = 0, 0
    
    def setcollideTurtle(self):
        self._collideTurtle=False
    
    def setBonus(self):
        self._bonus=True
    
    def setcollideRaft(self):
        self._collideRaft=False
    
    def setcollideRiver(self):
        self._collideRiver=False
    
    def setcollideCrocodile(self):
        self._collideRiver=False
    
    def collide(self, other):
        if isinstance(other, Crocodile):
            self._collideCrocodile=True
            self._collideRiver=True
            if self._x==0 or self._x==self._arena._w-self._w:
                #self._arena.remove(self)
                self._dead+=1
                if self._score>=50:
                    self._score-=50
                else:
                    self._score=0
                self._x, self._y = self._x_start, self._y_start
        
        if isinstance(other, Raft):
            self._collideRaft=True
            self._collideRiver=True
            if self._x==0 or self._x==self._arena._w-self._w:
                #self._arena.remove(self)
                self._dead+=1
                if self._score>=50:
                    self._score-=50
                else:
                    self._score=0
                self._x, self._y = self._x_start, self._y_start
        
        if isinstance(other, Turtle):
            self._collideTurtle=True
            self._collideRiver=True
            if self._x==0 or self._x==self._arena._w-self._w:
                #self._arena.remove(self)
                self._dead+=1
                if self._score>=80:
                    self._score-=80
                else:
                    self._score=0
                self._x, self._y = self._x_start, self._y_start
        
        if isinstance(other, Vehicle):
            #self._arena.remove(self)
            self._dead+=1
            if self._score>=80:
                self._score-=80
            else:
                self._score=0
            self._x, self._y = self._x_start, self._y_start
        
        if isinstance(other, River):
            self._collideRiver=True
            if self._collideRaft==False and self._collideTurtle==False and self._collideCrocodile==False:
                #self._arena.remove(self)
                self._dead+=1
                if self._score>=100:
                    self._score-=100
                else:
                   self._score=0
                self._x, self._y = self._x_start, self._y_start
            
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 13, 369, self._w, self._h
    
    def reset(self):
        self._dead=0
        self._areas = [False, False, False, False, False]
        self._x, self._y = self._x_start, self._y_start
        self._win=False
    
    def ctrl_win(self):
        if self._y==54:
            if self._x>=46 and self._x<=62 and self._areas[0]==False:
                self._score+=1000
                self._areas[0]=True
                self._x, self._y = self._x_start, self._y_start
            elif self._x>=174 and self._x<=190 and self._areas[1]==False:
                self._score+=1000
                self._areas[1]=True
                self._x, self._y = self._x_start, self._y_start
            elif self._x>=302 and self._x<=318 and self._areas[2]==False:
                self._score+=1000
                self._areas[2]=True
                self._x, self._y = self._x_start, self._y_start
            elif self._x>=430 and self._x<=446 and self._areas[3]==False:
                self._score+=1000
                self._areas[3]=True
                self._x, self._y = self._x_start, self._y_start
            elif self._x>=558 and self._x<=574 and self._areas[4]==False:
                self._score+=1000
                self._areas[4]=True
                self._x, self._y = self._x_start, self._y_start
            else:
                self._dead+=1
                self._x, self._y = self._x_start, self._y_start
        
        if self._areas[0]==True and self._areas[1]==True and self._areas[2]==True and self._areas[3]==True and self._areas[4]==True:
                self._win=True
            
