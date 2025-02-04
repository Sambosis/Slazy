C:\mygit\BLazy\repo\maze\maze_solver.py
Language detected: python
import collections
from typing import List, Tuple

def get_number_of_reachable_fields(
    grid: List[List[bool]], rows: int, columns: int, start_row: int, start_column: int
) -> int:
    """
    Calculates the number of reachable fields in the top row of a maze,
    starting from a given position.

    The player can move up, left, or right in the maze. Moving down is not allowed.
    The maze is represented by a 2D boolean array where True indicates a traversable
    space and False indicates a blocked space.

    Uses Breadth-First Search (BFS) to explore reachable positions.

    Args:
        grid: A 2D list of booleans representing the maze.
        rows: The number of rows in the grid.
        columns: The number of columns in the grid.
        start_row: The starting row index (0-indexed).
        start_column: The starting column index (0-indexed).

    Returns:
        The number of reachable fields in the top row (row index 0).

    Examples:
        >>> grid1 = [
        ...     [True, True, False],
        ...     [True, True, True],
        ...     [False, True, True]
        ... ]
        >>> get_number_of_reachable_fields(grid1, 3, 3, 1, 1)
        2

        >>> grid2 = [
        ...     [True, False, True],
        ...     [True, True, True],
        ...     [True, True, True]
        ... ]
        >>> get_number_of_reachable_fields(grid2, 3, 3, 2, 0)
        2

        >>> grid3 = [
        ...     [False, False, False],
        ...     [False, False, False],
        ...     [False, False, False]
        ... ]
        >>> get_number_of_reachable_fields(grid3, 3, 3, 0, 0)
        0

        >>> grid4 = [[]]
        >>> get_number_of_reachable_fields(grid4, 0, 0, 0, 0)
        0
    """

    # Handle edge cases: invalid input or empty grid
    if not grid or rows <= 0 or columns <= 0:
        return 0
    if start_row < 0 or start_row >= rows or start_column < 0 or start_column >= columns:
        return 0
    if not grid[start_row][start_column]:  # Starting position is blocked
        return 0

    visited = set()  # Set to keep track of visited positions (row, column)
    queue = collections.deque([(start_row, start_column)])  # Queue for BFS
    visited.add((start_row, start_column))
    reachable_top_row_fields = 0

    while queue:
        current_row, current_column = queue.popleft()

        if current_row == 0:
            reachable_top_row_fields += 1

        # Possible moves: up, left, right
        moves = [(-1, 0), (0, -1), (0, 1)]  # (row_change, column_change)

        for dr, dc in moves:
            next_row, next_column = current_row + dr, current_column + dc

            # Check if the next position is within grid boundaries
            if 0 <= next_row < rows and 0 <= next_column < columns:
                # Check if the next position is traversable and not visited
                if grid[next_row][next_column] and (next_row, next_column) not in visited:
                    visited.add((next_row, next_column))
                    queue.append((next_row, next_column))

    return reachable_top_row_fields
