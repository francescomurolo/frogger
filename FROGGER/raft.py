from random import choice, randrange
from actor import Actor, Arena

class Raft(Actor):
    def __init__(self, arena, x, y, type, dim):
        self._dim=dim
        self._type=type
        self._x, self._y = x, y
        if self._dim==1:
            self._w, self._h = 100, 23
            self._speed = 3
        elif self._dim==2:
            self._w, self._h = 120, 23
            self._speed = 1
        elif self._dim==3:
            self._w, self._h = 200, 23
            self._speed = 2
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
            return 7, 228, self._w, self._h
        elif self._dim==2:
            return 7, 198, self._w, self._h
        elif self._dim==3:
            return 7, 165, self._w, self._h
    
    def getSpeed(self):
        return self._speed