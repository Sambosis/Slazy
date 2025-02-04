C:\mygit\BLazy\repo\maze\maze_solver.py
Language detected: python
from collections import deque

def get_number_of_reachable_fields(grid, rows, columns, start_row, start_column):
    """
    This function implements a maze solver using BFS to find reachable fields in the top row.

    Args:
        grid (list): A 2D list representing the maze.
        rows (int): The number of rows in the maze.
        columns (int): The number of columns in the maze.
        start_row (int): The row index of the starting point.
        start_column (int): The column index of the starting point.

    Returns:
        int: The number of unique reachable fields in the top row.
    """

    # Create a visited set to keep track of visited cells
    visited = set((start_row, start_column))

    # Create a queue for BFS traversal and enqueue the starting point
    queue = deque([(start_row, start_column)])

    # Initialize a set to store the reachable fields in the top row
    reachable_fields = set()

    # Define the possible moves (up, left, right)
    moves = [(0, -1), (0, 1), (-1, 0)]

    # Perform BFS traversal
    while queue:
        row, column = queue.popleft()

        # If the current cell is in the top row, add it to the reachable fields set
        if row == 0:
            reachable_fields.add(column)

        # Explore the neighbors
        for dr, dc in moves:
            new_row, new_column = row + dr, column + dc

            # Check if the new position is within the grid boundaries
            if (0 <= new_row < rows) and (0 <= new_column < columns) and (new_row, new_column) not in visited:
                # Mark the new position as visited
                visited.add((new_row, new_column))

                # Enqueue the new position
                queue.append((new_row, new_column))

    # Return the number of unique reachable fields in the top row
    return len(reachable_fields)


# Test cases
grid1 = [
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0],
    [0, 1, 1, 0]
]
print(get_number_of_reachable_fields(grid1, 4, 4, 3, 0))  # Expected output: 2

grid2 = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0]
]
print(get_number_of_reachable_fields(grid2, 5, 7, 4, 0))  # Expected output: 5
