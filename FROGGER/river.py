from random import choice, randrange
from actor import Actor, Arena

class River(Actor):
    def __init__(self, arena):
        self._x, self._y = 0, 81
        self._w, self._h = 640, 160
        self._arena = arena
        arena.add(self)
    
    def move(self):
        pass
    
    def collide(self, other):
        pass
    
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 0, 80, self._w, self._h