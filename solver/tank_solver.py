from solver.base_solver import BaseSolver

class TankSolver(BaseSolver):
    # def solve_step(self) -> dict[str, list]:

    def solve_step(self) -> dict[str, list]:
        return {'safe': [], 'mines': []}  # Placeholder implementation
    
    def _get_border_tiles(self):
        border = set()
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if self.board.visible[r][c] == -1 and self._is_border(r, c):
                    border.add((r, c))
        return border
    
if __name__ == "__main__":
    from board.basic_board import BasicBoard
    board = BasicBoard(5, 10, 5)
    board.generate(2, 7)
    board.print_board()
    solver = TankSolver(board)
    print(solver._get_border_tiles())