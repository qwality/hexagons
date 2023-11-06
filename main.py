import pygame
# import json

from icecream import ic

from classes.coord      import Coord
from classes.color      import Color
from classes.ui         import UI
from classes.metadata   import metadata
from classes.game       import Game#, Hex
# from classes.grid       import Grid, Hex
from classes.hexagon    import Hexagon


def main():
    pygame.init()
    pygame.display.set_caption(metadata.name)

    ui = UI(metadata.width, metadata.height, bg_color=Color.dark_grey)

    game = Game(ui.surface, Color.soft_grey, 7, 7, 100, 5, 10, (150, 175, 200))
    ui.add_element(game)
    ui.add_updateble(game)
    ui.add_observer(game)

    offset = UI.Text(Coord(0,0),'offset: {0}', [game.controlls._offset], font_color=Color.white)
    ui.add_element(offset)
    zoom   = UI.Text(Coord(0,25), 'zoom: {0}', [game.controlls._zoom],   font_color=Color.white)
    ui.add_element(zoom)

    ic(game.params)

    py_clock = pygame.time.Clock()
    
    while ui.clock.running:

        ui.event_handler()
        ui.update()
        # ui.surface.blit(game.display(), game.controlls.offset)
        pygame.display.flip()
    
    py_clock.tick(ui.clock.frame_rate)


if __name__ == '__main__':
    main()


    