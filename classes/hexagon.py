import pygame

from dataclasses import dataclass
from pygame import Surface, Vector2
from math import sqrt, copysign
from typing import Type

from .color import Color
from icecream import ic

class Hexagon:
    # @dataclass
    class Block:
        active          : bool

        mouse_in        : bool
        mouse_pressed   : bool

        sprite          : Surface

        def __init__(self):
            self.active         = True
            self.mouse_in       = False
            self.mouse_pressed  = False
            self.sprite         = None

    class Mouse:
        @staticmethod
        def enter(instance: Type['Hexagon.Block']):
            instance.sprite.set_alpha(200)
            instance.mouse_in = True
            
        @staticmethod
        def leave(instance: Type['Hexagon.Block']):
            instance.sprite.set_alpha(255)
            instance.mouse_in = False

        @staticmethod
        def down(instance: Type['Hexagon.Block']):
            instance.mouse_pressed = True

        @staticmethod
        def up(instance: Type['Hexagon.Block']):
            if instance.mouse_in:   Hexagon.Mouse.enter(instance)
            else:                   Hexagon.Mouse.leave(instance)

            instance.mouse_pressed = False

    @staticmethod
    def calc_points(size: tuple[int,int], coord: tuple[int,int]=(0,0)) -> list[tuple[float,float]]:
        b, a = size
        a, b = 1/4*a, 1/2*b
        
        x0, y0 = coord

        x1, y1 = x0+b, y0+a
        x2, y2 = x1+b, y1+a
        y3     =       y2+a
        y4     =       y3+a
        
        return [
            (x0, y1),
            (x1, y0),
            (x2, y1),
            (x2, y3),
            (x1, y4),
            (x0, y3),
            (x0, y1)
        ]
    
    @staticmethod
    def round_points(points: tuple[tuple[float,float]]) -> list[tuple[int,int]]:
        return [(round(x), round(y)) for x,y in points]
    
    @staticmethod
    def draw(size: tuple[int,int], color: Color.ColorTuple, alpha: int=255, border: tuple[int,int]=(0,0)) -> Surface:
        width, height = Vector2(size) - Vector2(border)
        # ic(width, height, size, border)

        points      = Hexagon.calc_points((width, height))
        int_points  = Hexagon.round_points(points)

        surface = Surface((width+1, height+1), pygame.SRCALPHA)
        pygame.draw.polygon(surface, color + (alpha,), int_points)
        return surface

    @staticmethod
    def hex_dev(size: tuple[int,int], coord: tuple[int, int]) -> tuple[int, int]:
        """given real coord and size of hexagon outputs x,y position in grid of hexagons of given size"""
        Cx, Cy  = coord
        b, a    = size

        a, b = 1/2*a, 1/2*b

        Cx -= b
        Cy -= a

        denom = a*a + 4*b**2

        if denom <= 0 or b <= 0:
            raise ValueError(f'devision by 0: coord:{coord}, size:{size}')

        Ax = 2*b*(a*Cy   + 2*b*Cx) / denom
        Ay =   a*(a*Cy   + 2*b*Cx) / denom
        Bx = 2*b*(2*b*Cx -   a*Cy) / denom
        By =   a*(a*Cy   - 2*b*Cx) / denom

        A = (sqrt((Cy - Ay)**2+(Cx - Ax)**2)*copysign(1, Cy - Ay)) // b
        B = (sqrt((Cy - By)**2+(Cx - Bx)**2)*copysign(1, Cy - By)) // b
        X = Cx // b

        Gy = int((A + B + 2) // 3)
        Gx = int((X - Gy % 2 + 1) // 2)

        return Gx, Gy

    @staticmethod
    def hex_mul(size: tuple[int,int], pos: tuple[int,int]) -> tuple[int,int]:
        """given size of hexagon and position in hexagon grid, outputs real coord"""
        x, y = pos
        b, a = size
        a, b = 1/2*a, 1/2*b

        coord = (round(x * 2 * b + y % 2 * b),
                 round(y * 3 / 2 * a ))

        return coord
 
    @staticmethod
    def blit(surface: Surface, pos: tuple[int,int], size: tuple[int,int], sprite: Surface) -> None:
        surface.blit(sprite, Hexagon.hex_mul(size, pos))
    
    @staticmethod
    def blits(surface: Surface, iterable: tuple[tuple[int,int,Block]], size: tuple[int,int]) -> None:
        surface.blits(((block.sprite, Hexagon.hex_mul(size, (x,y))) for x, y, block in iterable))

