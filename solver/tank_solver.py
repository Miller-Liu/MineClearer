from solver.base_solver import BaseSolver

class TankSolver(BaseSolver):
    # def solve_step(self) -> dict[str, list]:

    def solve_step(self) -> dict[str, list]:
        components = self._get_border_tiles()
        safe = []
        mines = []
        
        return {'safe': safe, 'mines': mines}  # Placeholder implementation
    
    def _get_border_tiles(self):
        border = set()
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if self.board.visible[r][c] == -1 and self._is_border(r, c):
                    border.add((r, c))
        
        # segregate border tiles into connected components
        components = []
        while border:
            region = []
            queue = [border.pop()]

            while queue:
                tile = queue.pop()
                region.append(tile)

                # numbered neighbors of this tile
                numbered = {
                    (nr, nc)
                    for nr, nc in self._neighbors(*tile)
                    if self.board.visible[nr][nc] > 0
                }

                for number in numbered:
                    for neighbor in self._neighbors(*number):
                        if neighbor in border and neighbor not in queue:
                            queue.append(neighbor)
                            border.remove(neighbor)
            
            components.append(region)
        
        return components
    
    def test_bombs(self, bombs):
        """
        Test if a given bomb placement is valid with respect to the current board state.
        bombs: set of (row, col) tuples representing bomb placements
        Returns True if valid, False otherwise.
        """
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if self.board.visible[r][c] > 0:
                    # Count bombs in the neighborhood
                    count = sum(
                        ((nr, nc) in bombs or self.board.visible[nr][nc] == -2) 
                        for nr, nc in self._neighbors(r, c)
                    )
                    if count != self.board.visible[r][c]:
                        return False
        return True
    
if __name__ == "__main__":
    from board.basic_board import BasicBoard
    board = BasicBoard(5, 10, 5)
    board.generate(2, 7)
    board.print_board()
    solver = TankSolver(board)
    print(solver._get_border_tiles())