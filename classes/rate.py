from numpy import *
from classes.block import Block

class Rate():
    __slots__ = ('block','func','min_vel','max_vel','a','b','c','d')

    def __init__(self, block=None, func=None, min_vel=None, max_vel=None, a=None, b=None, c=None, d=None):
        self.block      :Block  = block
        self.func       :str    = func
        self.min_vel    :float  = min_vel
        self.max_vel    :float  = max_vel
        self.a          :float  = a
        self.b          :float  = b
        self.c          :float  = c
        self.d          :float  = d

    def to_dict(self):
        return {"min":self.min_vel,
                "max":self.max_vel,
                self.func:{
                    'a':self.a,
                    'b':self.b,
                    'c':self.c,
                    'd':self.d
                }}
    
    def to_ai_ready(self):
        return array([self.a,self.b,self.c,self.d])