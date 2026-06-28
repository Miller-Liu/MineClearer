from abc import ABC, abstractmethod
from board.basic_board import BasicBoard


class BaseSolver(ABC):
    def __init__(self, board : BasicBoard):
        self.board = board

    @abstractmethod
    def solve_step(self) -> dict[str, list]:
        """
        Returns {safe : list, mines : list} — lists of (row, col) tuples.
        safe  → cells confirmed mine-free, ready to reveal
        mines → cells confirmed to be mines, ready to flag
        """
        pass

    def _neighbors(self, row, col) -> list:
        result = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.board.rows and 0 <= c < self.board.cols:
                    result.append((r, c))
        return result
    
    def _is_border(self, row, col) -> bool:
        '''
        Returns if a tile (either number or hidden) is on the border.
        A tile is a border tile if its neighborhood contains both hidden and number tiles
        '''
        
        if self.board.visible[row][col] == 0:
            return False

        has_number, has_hidden = False, False
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                r, c = row + dr, col + dc
                if 0 <= r < self.board.rows and 0 <= c < self.board.cols:
                    if self.board.visible[r][c] > 0:
                        has_number = True
                    if self.board.visible[r][c] == -1:
                        has_hidden = True
                    if has_number and has_hidden:
                        return True 
        return False