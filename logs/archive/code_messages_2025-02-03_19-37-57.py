C:\mygit\BLazy\repo\maze\maze_solver.py
Language detected: python
import collections

def GetNumberOfReachableFields(grid: list[list[bool]], rows: int, columns: int, startRow: int, startColumn: int) -> int:
    """
    Finds the number of reachable fields in the top row (row 0) of a grid using BFS.

    Args:
        grid: 2D array where True means traversable, False means blocked.
        rows: Number of rows in grid.
        columns: Number of columns in grid.
        startRow: Starting row position.
        startColumn: Starting column position.

    Returns:
        The number of reachable fields in the top row (row 0).
    """

    if not grid or rows == 0 or columns == 0:
        return 0  # Handle empty grid or dimensions

    if not 0 <= startRow < rows or not 0 <= startColumn < columns:
        return 0 # Handle invalid start position

    if not grid[startRow][startColumn]:
        return 0 # Handle blocked start position

    visited = [[False for _ in range(columns)] for _ in range(rows)]
    queue = collections.deque([(startRow, startColumn)])
    visited[startRow][startColumn] = True
    reachable_in_top_row = 0

    while queue:
        row, col = queue.popleft()

        if row == 0:
            reachable_in_top_row += 1

        # Possible movements: up, left, right
        moves = [(-1, 0), (0, -1), (0, 1)]

        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < rows and 0 <= new_col < columns and grid[new_row][new_col] and not visited[new_row][new_col]:
                visited[new_row][new_col] = True
                queue.append((new_row, new_col))

    reachable_top_row_count = 0
    for c in range(columns):
        if visited[0][c]:
            reachable_top_row_count += 1
    return reachable_top_row_count


if __name__ == '__main__':
    # Test case 1: Example from description
    grid1 = [
        [True, True, False, True],
        [True, True, True, True],
        [True, False, True, True]
    ]
    rows1 = 3
    columns1 = 4
    startRow1 = 2
    startColumn1 = 0
    expected1 = 3 # Columns 0, 1, 3 in row 0 should be reachable
    result1 = GetNumberOfReachableFields(grid1, rows1, columns1, startRow1, startColumn1)
    print(f"Test Case 1 - Grid 1: Expected {expected1}, Got {result1}, {'Pass' if result1 == expected1 else 'Fail'}")

    # Test case 2: Start in top row
    grid2 = [
        [True, True, True, True],
        [True, True, True, True],
        [True, False, True, True]
    ]
    rows2 = 3
    columns2 = 4
    startRow2 = 0
    startColumn2 = 0
    expected2 = 4 # All cells in row 0 are reachable
    result2 = GetNumberOfReachableFields(grid2, rows2, columns2, startRow2, startColumn2)
    print(f"Test Case 2 - Start in top row: Expected {expected2}, Got {result2}, {'Pass' if result2 == expected2 else 'Fail'}")

    # Test case 3: No path to top row
    grid3 = [
        [True, False, True, True],
        [True, False, True, True],
        [True, False, True, True]
    ]
    rows3 = 3
    columns3 = 4
    startRow3 = 2
    startColumn3 = 0
    expected3 = 0 # No path to top row because of the column of Falses
    result3 = GetNumberOfReachableFields(grid3, rows3, columns3, startRow3, startColumn3)
    print(f"Test Case 3 - No path to top row: Expected {expected3}, Got {result3}, {'Pass' if result3 == expected3 else 'Fail'}")

    # Test case 4: Blocked start
    grid4 = [
        [True, True, True, True],
        [True, True, True, True],
        [False, False, True, True]
    ]
    rows4 = 3
    columns4 = 4
    startRow4 = 2
    startColumn4 = 0
    expected4 = 0 # Start is blocked
    result4 = GetNumberOfReachableFields(grid4, rows4, columns4, startRow4, startColumn4)
    print(f"Test Case 4 - Blocked start: Expected {expected4}, Got {result4}, {'Pass' if result4 == expected4 else 'Fail'}")

    # Test case 5: Single cell grid, start at 0,0
    grid5 = [[True]]
    rows5 = 1
    columns5 = 1
    startRow5 = 0
    startColumn5 = 0
    expected5 = 1
    result5 = GetNumberOfReachableFields(grid5, rows5, columns5, startRow5, startColumn5)
    print(f"Test Case 5 - Single cell grid: Expected {expected5}, Got {result5}, {'Pass' if result5 == expected5 else 'Fail'}")

    # Test case 6: Single row grid
    grid6 = [[True, True, True]]
    rows6 = 1
    columns6 = 3
    startRow6 = 0
    startColumn6 = 1
    expected6 = 3
    result6 = GetNumberOfReachableFields(grid6, rows6, columns6, startRow6, startColumn6)
    print(f"Test Case 6 - Single row grid: Expected {expected6}, Got {result6}, {'Pass' if result6 == expected6 else 'Fail'}")

    # Test case 7: All False grid (just to be thorough, though start position should handle it)
    grid7 = [[False, False], [False, False]]
    rows7 = 2
    columns7 = 2
    startRow7 = 1
    startColumn7 = 1
    expected7 = 0
    result7 = GetNumberOfReachableFields(grid7, rows7, columns7, startRow7, startColumn7)
    print(f"Test Case 7 - All False grid: Expected {expected7}, Got {result7}, {'Pass' if result7 == expected7 else 'Fail'}")
