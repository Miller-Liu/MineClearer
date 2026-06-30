from solver.base_solver import BaseSolver
from collections import Counter

class TankSolver(BaseSolver):
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


    def test_bombs_partial(self, bombs):
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
                    if count > self.board.visible[r][c]:
                        return False
        return True
    

    def _recurse(self, component, depth, current_bombs : set, solutions: list):
        # prune early if already invalid
        if not self.test_bombs_partial(current_bombs):
            return
        
        # base case — full assignment, check validity
        if depth == len(component):
            if self.test_bombs(current_bombs):
                solutions.append([tile for tile in component if tile in current_bombs])
                
                # print("-" * 20)
                # self.board.print_test_board(current_bombs)
                # print(current_bombs)
                # input()
            return
        
        tile = component[depth]
        
        # branch 1: tile is a mine
        current_bombs.add(tile)
        self._recurse(component, depth + 1, current_bombs, solutions)
        current_bombs.remove(tile)
        
        # branch 2: tile is safe
        self._recurse(component, depth + 1, current_bombs, solutions)


    def solve_step(self) -> dict[str, list]:
        components = self._get_border_tiles()
        safe = []
        mines = []

        for component in components:
            solutions = []
            self._recurse(component, 0, set(), solutions)
            print(solutions)
            
            # a tile is definitely a mine if it's a mine in ALL solutions
            # a tile is definitely safe if it's a mine in NO solutions
            mine_count = Counter({tile: 0 for tile in component})
            mine_count.update(tile for solution in solutions for tile in solution)
            
            for tile in component:
                if mine_count[tile] == len(solutions):
                    mines.append(tile)
                elif mine_count[tile] == 0:
                    safe.append(tile)
        
        return {'safe': safe, 'mines': mines} 
    
if __name__ == "__main__":
    from board.basic_board import BasicBoard
    board = BasicBoard(5, 10, 10, seed=2)
    board.generate(2, 9)
    board.print_board()
    solver = TankSolver(board)
    print(solver._get_border_tiles())
    print(solver.solve_step())