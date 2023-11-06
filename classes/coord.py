from typing import Any, Iterable

class Coord(): 
    dimensions = 'xyzt'

    def __init__(self, *args: Iterable[int | float], **kwargs):
        self._value = args

    def __repr__(self):
        return f'coord:{self._value}'
    
    def __str__(self):
        return f'{self._value}'

    def __iter__(self):
        return iter(self._value)

    # def __set__(self, instance, value):
    #     print('set')
    #     self._value = tuple(value)

    def set(self, value):
        self._value = tuple(value)

    def __getitem__(self, key):
        return self._value[key]
    
    def __setitem__(self, key, value):
        self._value = self._value[:key] + (value,) + self._value[key + 1:]

    def __getattr__(self, name):
        if name in self.dimensions:
            i = self.dimensions.index(name)
            return self._value[i]
        else:
            raise ValueError
    
    def __setatribute__(self, __name: str, __value):
        # if __name == '_value':
        #     self.__dict__[__name] = tuple(__value)
        if __name in self.dimensions:
            i = self.dimensions.index(__name)
            self._value = self._value[:i] + (__value,) + self._value[i + 1:]
        else:
            raise ValueError

    # def __setattr__(self, __name: str, __value):
    #     if __name == '_value':
    #         self.__dict__[__name] = tuple(__value)
    #     elif __name in self.dimensions:
    #         i = self.dimensions.index(__name)
    #         self._value = self._value[:i] + (__value,) + self._value[i + 1:]
    #     else:
    #         raise ValueError
        

    def __eq__(self, other):
        if isinstance(other, Coord):
            return self._value == other._value
        else: raise NotImplemented
    
    def __add__(self, other):
        return Coord(*(a + b for a, b in zip(self._value, other)))
    
    def __sub__(self, other):
        return Coord(*(a - b for a, b in zip(self._value, other)))

    def __iadd__(self, other):
        self._value = tuple(a + b for a, b in zip(self._value, other))
        return self

    def __isub__(self, other):
        self._value = tuple(a - b for a, b in zip(self._value, other))
        return self
    
    def __mul__(self, other):
        return Coord(*(i * other for i in self._value))
    
    def __truediv__(self, other):
        return Coord(*(i / other for i in self._value))

