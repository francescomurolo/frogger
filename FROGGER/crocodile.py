from random import choice, randrange
from actor import Actor, Arena

class Crocodile(Actor):
    def __init__(self, arena, x, y):
        self._speed=2
        self._x, self._y = x, y
        self._w, self._h = 90,20
        self._dx, self._dy = self._speed, self._speed
        self._arena = arena
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        self._x += self._dx
        if self._x > arena_w+self._w:
            self._x=(-arena_w/100*40)+self._w
            
    def collide(self, other):
        pass
    
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 156, 374, self._w, self._h
    
    def getSpeed(self):
        return self._speed