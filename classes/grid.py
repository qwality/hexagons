from typing     import Generator
from numpy      import clip

from .hexagon   import Hexagon

BLOCK = Hexagon.Block
    
class Grid:
    def __init__(self, cols: int, rows: int, fill_type=BLOCK) -> None:
        self.__arr_2D: list[list[fill_type]] = [[fill_type() for x in range(cols)] for y in range(rows)]
        self._cols, self._rows = cols, rows
    
    @property
    def size(self):
        return self._cols, self._rows

    def clip(self, col, row) -> tuple[int,int]:
        return clip(col, 0, self._cols - 1), clip(row, 0, self._rows - 1)
    
    def __iter__(self) -> Generator[tuple[int, int, BLOCK], None, None]:
        for y, row in enumerate(self.__arr_2D):
            for x, col in enumerate(row):
                yield x, y, col

    def __getitem__(self, row) -> list[BLOCK]:
        return self.__arr_2D[row]
    
    def __call__(self, col, row) -> BLOCK:
        if self.__arr_2D[row][col] is not None:
            return self.__arr_2D[row][col]
        else:
            raise ValueError(f'grid at: ({col}, {row}) is None')
    


        

    

