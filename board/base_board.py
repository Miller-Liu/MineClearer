from abc import ABC, abstractmethod

class BaseBoard(ABC):
    def __init__(self, rows, cols, num_mines, seed=None):
        '''
        Initialize the board with the given dimensions and number of mines.
        '''
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.mines = [[False]*cols for _ in range(rows)]
        self.seed = seed

        '''
        -1 : hidden
        -2 : flagged
        0 : empty
        1 - 8 : number of adjacent mines
        '''
        self.visible = [[-1]*cols for _ in range(rows)]

    @abstractmethod
    def generate(self, exclude_row, exclude_col):
        '''
        Initialize the board with mines placed.
        '''
        pass

    def adjacent_mines(self, row, col):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    if self.mines[r][c]:
                        count += 1
        return count

    def reveal(self, row, col):
        if self.mines[row][col]:
            return False

        queue = [(row, col)]
        self.visible[row][col] = self.adjacent_mines(row, col)  # mark immediately

        while queue:
            r, c = queue.pop()
            if self.visible[r][c] != 0:  # only expand from empty cells
                continue
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.visible[nr][nc] == -1:  # only enqueue hidden cells
                            self.visible[nr][nc] = self.adjacent_mines(nr, nc)
                            queue.append((nr, nc))
        return True
    
    def print_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.visible[r][c] == -1:
                    print('.', end=' ')
                elif self.visible[r][c] == -2:
                    print('F', end=' ')
                else:
                    print(self.visible[r][c], end=' ')
            print()
    
    def print_test_board(self, bombs):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in bombs:
                    print('B', end=' ')
                elif self.visible[r][c] == -1:
                    print('.', end=' ')
                elif self.visible[r][c] == -2:
                    print('F', end=' ')
                else:
                    print(self.visible[r][c], end=' ')
            print()