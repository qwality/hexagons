import pygame
import cairo
from pygame import Surface, Vector2
from math import ceil

from .coord import Coord
from .clock import Clock
from .color import Color
from abc import ABC, abstractmethod
# from .game  import Game
from icecream import ic

class UI:
    class Updatable:
        def update(self) -> None:
            pass

    class Observer:
        def event_listener(self, event) -> None:
            pass

    class Element:
        def __init__(self, surface: Surface, coord: Coord) -> None:
            self.surface = surface
            self.coord   = coord

        def display(self):
            pass

    class Element2(ABC):
        def __init__(self, coord: Vector2) -> None:
            super().__init__()
            self.coord   = coord

        @abstractmethod
        def get_surface(self) -> Surface:
            pass


    class _Size:
        @property
        def size(self):
            return (self.width, self.height)
        @size.setter
        def size(self, value):
            self.width, self.height = value

        def __init__(self, width: int, height: int) -> None:
            self.size = (width, height)

    class _Font:
        def __init__(self, font_size: int=36, font_color=Color.black) -> None:
            self.font_color     = font_color
            self.__font_size    = font_size
            self.font           = pygame.font.Font(None, font_size)

    class _FillColor:
        def __init__(self, fill_color=Color.white, alpha=(255,)) -> None:
            self.fill_color = fill_color
            self.alpha      = alpha

    class Text(Element2, _Font, _Size):
        @property
        def size(self):
            return self.font.size(self.msg)
        
        @size.setter
        def size(self, value):
            raise ValueError('size of text is read only')

        def __init__(self, coord: Coord, text: str='', data: list[any]=[], font_size: int=36, font_color=Color.black) -> None:
            UI.Element2.__init__(self, coord)
            UI._Font.__init__(self, font_size, font_color)
            self.text = text
            self.data = data

        @property
        def msg(self):
            return self.text.format(*self.data)
        
        def get_surface(self) -> Surface:
            return self.font.render(self.msg, True, self.font_color)
        

    __observers  :list[Observer]  = []
    __elements   :list[Element2]   = []
    __updatables :list[Updatable] = []
    __instance                    = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(UI, cls).__new__(cls)
        return cls.__instance
    
    @property
    def size(self):
        return (self.width, self.height)
    
    @size.setter
    def size(self, size):
        self.width, self.height = size

    @staticmethod
    def mouse_pos():
        return pygame.mouse.get_pos()
    
    clock   :Clock   = None
    surface :Surface = None
    bg_color         = Color.black

    def __init__(self, width:int, height:int, clock:Clock=Clock(1, 60), bg_color=Color.black):
        self.size       = (width, height)
        self.clock      = clock
        self.surface    = pygame.display.set_mode(self.size)
        self.bg_color   = bg_color

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.clock.running = False
            else:
                for observer in self.__observers:
                    observer.event_listener(event)

    def update(self):
        with self.clock as tick:
            if tick:
                for updatable in self.__updatables:
                    updatable.update()
            self.display()

    def display(self):
        self.surface.fill(self.bg_color)
        for element in self.__elements:
            self.surface.blit(element.get_surface(), tuple(element.coord))
        pass


    def add_element(self, element: Element):
        self.__elements.append(element)

    def add_observer(self, observer: Observer):
        self.__observers.append(observer)

    def add_updateble(self, updatable: Updatable):
        self.__updatables.append(updatable)