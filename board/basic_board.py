from board.base_board import BaseBoard
import random

class BasicBoard(BaseBoard):
    def generate(self, exclude_row, exclude_col):
        '''
        Randomly place mines on the board. 
        '''
        exclude_bomb = set()
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r = exclude_row + dr
                c = exclude_col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    exclude_bomb.add((r, c))
        candidates = [
            (r, c) for r in range(self.rows)
                    for c in range(self.cols)
                    if (r, c) not in exclude_bomb
        ]
        random.seed(self.seed)
        for r, c in random.sample(candidates, self.num_mines):
            self.mines[r][c] = True
        self.reveal(exclude_row, exclude_col)


if __name__ == "__main__":
    board = BasicBoard(5, 10, 5, seed=42)
    board.generate(2, 7)
    board.reveal(0, 0)
    board.print_board()