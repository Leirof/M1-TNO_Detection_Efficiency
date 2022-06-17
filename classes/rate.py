from numpy import *

class Rate():
    __slots__ = ('parent','func','min_vel','max_vel','a','b','c','d')

    all = []

    def __init__(self, parent=None, func=None, min_vel=None, max_vel=None, a=None, b=None, c=None, d=None):
        self.parent             = parent
        self.func       :str    = func
        self.min_vel    :float  = min_vel
        self.max_vel    :float  = max_vel
        self.a          :float  = a
        self.b          :float  = b
        self.c          :float  = c
        self.d          :float  = d
        Rate.all.append(self)

    def to_dict(self):
        return {"min":self.min_vel,
                "max":self.max_vel,
                self.func:{
                    'a':self.a,
                    'b':self.b,
                    'c':self.c,
                    'd':self.d
                }}
    
    def to_ai_ready(self, **kwargs):
        return array([self.a,self.b,self.c,self.d])