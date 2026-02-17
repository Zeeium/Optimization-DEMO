import random


rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))
num_reactors = int(input("Enter number of reactors to place: "))
radius = int(input("Enter reactor radius: "))
min_val = int(input("Enter minimum grid demand value: "))
max_val = int(input("Enter maximum grid demand value: "))


grid = [[random.randint(min_val, max_val) for _ in range(cols)] for _ in range(rows)]

# Majority of these functions are just for testing.
# Just hit run. 
# The correct function calls have already been made at the bottom.


def print_grid(grid):
    print("\nGenerated Grid:")
    for row in grid:
        print(" ".join(f"{v:2}" for v in row))
    print()

print_grid(grid)


def get_coverage_cells(row, col, radius):
    coverage_cells = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if abs(r - row) + abs(c - col) <= radius:
                coverage_cells.append((r, c))
    return coverage_cells

def covered_demand(row, col, radius):
    cells = get_coverage_cells(row, col, radius)
    return sum(grid[r][c] for r, c in cells)

def place_reactors(grid, num_reactors, radius):
    placed_reactors = []
    remaining_demand = [row.copy() for row in grid]

    for _ in range(num_reactors):
        best_cell = None
        max_covered = -1

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                coverage = get_coverage_cells(row, col, radius)
                covered = sum(remaining_demand[r][c] for r, c in coverage)
                if covered > max_covered:
                    max_covered = covered
                    best_cell = (row, col)

        if best_cell is None:
            break

        placed_reactors.append(best_cell)

        
        for r, c in get_coverage_cells(*best_cell, radius):
            remaining_demand[r][c] = 0

    print(f"\nPlaced reactors at: {placed_reactors}\n")
    return placed_reactors

# This is the greedy algorithm, slightly modified so it works for online IDE execution
def print_final_coverage(grid, placed_reactors, radius):
    print("Final Coverage Map (X = reactor, O = covered cell, . = not covered):\n")
    for r in range(rows):
        row_chars = []
        for c in range(cols):
            if (r, c) in placed_reactors:
                row_chars.append("X")
            else:
                covered = any(abs(r - rr) + abs(c - cc) <= radius for rr, cc in placed_reactors)
                row_chars.append("O" if covered else ".")
        print(" ".join(row_chars))

    
    total = sum(sum(row) for row in grid)
    covered_cells = set()
    for rr, cc in placed_reactors:
        for r, c in get_coverage_cells(rr, cc, radius):
            covered_cells.add((r, c))
    covered = sum(grid[r][c] for r, c in covered_cells)

    print(f"\nTotal demand covered: {covered}/{total} ({covered/total:.1%})")


placed = place_reactors(grid, num_reactors, radius)
print_final_coverage(grid, placed, radius)
