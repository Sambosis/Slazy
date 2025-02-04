C:\mygit\BLazy\repo\maze\maze_solver.py
Language detected: python
from collections import deque

def GetNumberOfReachableFields(grid, rows, cols, start_row, start_col):
    """
    This function uses BFS to find all reachable positions from the starting point
    in a given grid and counts how many positions in the top row are reachable.
    
    Parameters:
    grid (2D boolean array): The input grid where True represents an open field and False represents a blocked field
    rows (int): The number of rows in the grid
    cols (int): The number of columns in the grid
    start_row (int): The row of the starting point
    start_col (int): The column of the starting point
    
    Returns:
    int: The number of reachable positions in the top row
    """

    # Check if the start position is out of bounds or blocked
    if start_row < 0 or start_row >= rows or start_col < 0 or start_col >= cols or not grid[start_row][start_col]:
        return 0

    # Directions for valid moves (up, left, right)
    directions = [(-1, 0), (0, -1), (0, 1)]

    # Initialize a visited set to keep track of visited cells
    visited = set((start_row, start_col))

    # Initialize a queue for BFS with the starting point
    queue = deque([(start_row, start_col)])

    # Initialize a count of reachable positions in the top row
    count = 0

    # Perform BFS
    while queue:
        x, y = queue.popleft()

        # If the current position is in the top row, increment the count
        if x == 0:
            count += 1

        # Explore all valid moves from the current position
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if the new position is within bounds, not blocked, and not visited
            if (0 <= nx < rows) and (0 <= ny < cols) and grid[nx][ny] and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))

    return count

def main():
    # Test cases
    grid1 = [
        [True, False, True, True],
        [True, True, True, False],
        [True, False, True, True],
        [True, True, True, True]
    ]
    print(GetNumberOfReachableFields(grid1, 4, 4, 3, 0))  # Expected output: 2

    grid2 = [
        [True, True, True],
        [False, False, False],
        [True, True, True]
    ]
    print(GetNumberOfReachableFields(grid2, 3, 3, 2, 0))  # Expected output: 2

    grid3 = [
        [True],
        [False],
        [True]
    ]
    print(GetNumberOfReachableFields(grid3, 3, 1, 2, 0))  # Expected output: 1

if __name__ == '__main__':
    main()
