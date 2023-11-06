import pygame

from pygame import Surface, Vector2
from math   import sqrt
from numpy  import clip
from dataclasses import dataclass
from icecream import ic

from .grid  import Grid
from .ui    import UI
from .coord import Coord
from .pointer_wraper import Mutable
from .hexagon import Hexagon
from .color import Color

BLOCK = Hexagon.Block

class Game(UI.Element, UI._Size, UI.Observer, UI.Updatable, UI._FillColor):
    def __init__(self, window: Surface, fill_color, rows: int, cols: int, hex_size: tuple[int], hex_border: int, zoom_speed:int , alpha_modes: tuple[int,int,int]=(200,170,150)) -> None:

        
        self.grid       = Grid(rows, cols)

        self.params     = Game.Params(hex_size, hex_border, zoom_speed, alpha_modes)
        self.controlls  = Game.Controlls(self)

        self.gb_surface = Surface((int(self.params.hex_size.x * (cols+0.5)), int((self.params.hex_size.y*0.75) * (rows+0.25))))
        
        for x, y, _ in self.grid:
            self.grid[y][x].sprite = Hexagon.draw(self.params.hex_size, fill_color, border=self.params.hex_border)
            # self.grid[y][x] = Hex(fill_color)
            # self.grid[y][x].element = UI.Hexagon.draw(Coord(*self.controlls.hex_size) - self.controlls.hex_border, fill_color)

        Hexagon.blits(self.gb_surface, self.grid, self.params.hex_size)

    @property
    def coord(self):
        return self.controlls.offset

    @dataclass
    class Params:
        hex_size    : Vector2
        hex_border  : Vector2

        zoom_speed  : int
        alpha_modes : tuple[int,int,int]

        def __init__(self, hex_size: Vector2, hex_border: Vector2, zoom_speed: int, alpha_modes: tuple[int,int,int]):
            sqrt3_2 = 0.86
            self.hex_size    = Vector2(round(hex_size*sqrt3_2), hex_size)
            self.hex_border  = Vector2(round(hex_border*sqrt3_2), hex_border)
            self.zoom_speed  = zoom_speed
            self.alpha_modes = alpha_modes

    @dataclass
    class Controlls:
        _mouseover : BLOCK
        _pressed   : BLOCK

        _dragging         : bool
        _last_mouse_coord : Vector2
        _last_offset      : Vector2
        _offset           : Vector2
        _zoom             : Mutable

        def __init__(self, game):
            self._mouseover = None
            self._pressed   = None

            self._dragging         = False
            self._last_mouse_coord = Vector2(0,0)
            self._last_offset      = Vector2(0,0)
            self._offset           = Vector2(0,0)
            self._zoom             = Mutable(100)
            self._game: Game       = game
        
        @property
        def zoom(self) -> int:
            return self._zoom.get()
        
        @zoom.setter
        def zoom(self, value):
            self._zoom.set(clip(value, self._game.params.zoom_speed, None))
            
        @property
        def offset(self) -> Vector2:
            return self._offset
        
        @offset.setter
        def offset(self, value: Vector2):
            self._offset.update(value)

        @property
        def dragging(self) -> bool:
            if self._dragging: self.offset = Vector2(UI.mouse_pos()) - self._last_mouse_coord + self._last_offset
            return self._dragging
        
        @dragging.setter
        def dragging(self, value):
            self._dragging = value
            if value:
                self._last_mouse_coord = UI.mouse_pos()
            else:
                self._last_offset = self._offset.copy()
            
        @property
        def mouseover(self) -> BLOCK:
            return self._mouseover

        @mouseover.setter
        def mouseover(self, new_block: BLOCK):
            if self._mouseover is not new_block:
                if self._mouseover is not None:
                    Hexagon.Mouse.leave(self._mouseover)
                    # self._game.gb_surface.blit(new_block.sprite, new_block.sprite.get_offset())

                Hexagon.Mouse.enter(new_block)
                self._mouseover = new_block

        @property
        def pressed(self) -> BLOCK:
            return self._pressed
        
        @pressed.setter
        def pressed(self, new_hex: BLOCK):
            if new_hex is None:
                Hexagon.Mouse.up(self.pressed)
            else:
                Hexagon.Mouse.down(self.mouseover)
                        
            self._pressed = new_hex
    
    def update_mouseover(self) -> None:
        def get_clipped_mouse_pos() -> tuple[int, int]:
            return self.grid.clip(*Hexagon.hex_dev(self.params.hex_size, UI.mouse_pos() - self.controlls.offset))
        
        def get_Hex_at_mouse_pos() -> BLOCK:
            x, y = get_clipped_mouse_pos()
            return self.grid[y][x]
        
        self.controlls.mouseover = get_Hex_at_mouse_pos()

    def event_listener(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.MOUSEMOTION:
                                            self.update_mouseover()
                                            self.controlls.dragging
            case pygame.MOUSEBUTTONDOWN:
                if event.button == 1 :      self.controlls.pressed  = self.controlls.mouseover
                if event.button == 3 :      self.controlls.dragging = True
                if event.button == 4 :    
                                            self.controlls.zoom = self.controlls.zoom + self.params.zoom_speed
                if event.button == 5 :
                                            self.controlls.zoom = self.controlls.zoom - self.params.zoom_speed
            case pygame.MOUSEBUTTONUP:
                if event.button == 1 :      self.controlls.pressed  = None
                if event.button == 3 :      self.controlls.dragging = False
            case pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    print('a')

    def get_surface(self):
        self.gb_surface.fill(Color.black)
        Hexagon.blits(self.gb_surface, self.grid, self.params.hex_size)
        return pygame.transform.scale_by(self.gb_surface, self.controlls.zoom / 100)

    def display(self):
        # self.gb_surface.fill(Color.black)
        # Hexagon.blits(self.gb_surface, self.grid, self.params.hex_size)
        transformed = pygame.transform.scale_by(self.gb_surface, self.controlls.zoom / 100)

        return transformed
        # self.gb_surface
        # self.gb_surface.blits((hex.element, tuple(Coord(*self.controlls.hex_border) / 2 + UI.Hexagon.hex_multiplication((x,y), self.controlls.hex_size))) for x,y,hex in self.grid)
