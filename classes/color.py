from dataclasses import dataclass, astuple
from random import choice

@dataclass
class Color:
    @dataclass
    class ColorTuple:
        r: int
        g: int
        b: int

    black       :ColorTuple = ( 10,  0,  0)
    soft_grey   :ColorTuple = ( 60, 62, 65)
    dark_grey   :ColorTuple = ( 35, 32, 30)
    white       :ColorTuple = (255,255,255)
    red         :ColorTuple = (220, 40, 30)
    green       :ColorTuple = ( 30,200, 40)
    blue        :ColorTuple = ( 30, 40,200)
    yellow      :ColorTuple = (255,220,  0)

    __instance = None

    @dataclass
    class ColorTuple:
        r: int
        g: int
        b: int

    @classmethod
    def lighter(cls, color, factor):
        return tuple(max(0, i - factor) for i in color)
    
    @classmethod
    def darker(cls, color, factor):
        return tuple(min(255, i + factor) for i in color)

    @classmethod
    def get_random(cls):
        return choice(cls.colors)

    @classmethod
    @property
    def colors(cls):
        if cls.__instance is None: cls.__instance = Color()
        return astuple(cls.__instance)
    
# print(Color.get_random())