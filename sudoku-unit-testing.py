from itertools import product

def solve_sudoku(size, grid):
    """ An Sudoku solver using and efficient algorithm.
    >>> grid = [
    ...     [5, 3, 0, 0, 7, 0, 0, 0, 0],
    ...     [6, 0, 0, 1, 9, 5, 0, 0, 0],
    ...     [0, 9, 8, 0, 0, 0, 0, 6, 0],
    ...     [8, 0, 0, 0, 6, 0, 0, 0, 3],
    ...     [4, 0, 0, 8, 0, 3, 0, 0, 1],
    ...     [7, 0, 0, 0, 2, 0, 0, 0, 6],
    ...     [0, 6, 0, 0, 0, 0, 2, 8, 0],
    ...     [0, 0, 0, 4, 1, 9, 0, 0, 5],
    ...     [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    >>> for solution in solve_sudoku((3, 3), grid):
    ...     print(*solution, sep='\\n')
    [5, 3, 4, 6, 7, 8, 9, 1, 2]
    [6, 7, 2, 1, 9, 5, 3, 4, 8]
    [1, 9, 8, 3, 4, 2, 5, 6, 7]
    [8, 5, 9, 7, 6, 1, 4, 2, 3]
    [4, 2, 6, 8, 5, 3, 7, 9, 1]
    [7, 1, 3, 9, 2, 4, 8, 5, 6]
    [9, 6, 1, 5, 3, 7, 2, 8, 4]
    [2, 8, 7, 4, 1, 9, 6, 3, 5]
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
    """
    R, C = size
    N = R * C
    A = ([("r_c", rc) for rc in product(range(N), range(N))] +
         [("r_n", rn) for rn in product(range(N), range(1, N + 1))] +
         [("c_n", cn) for cn in product(range(N), range(1, N + 1))] +
         [("b_n", bn) for bn in product(range(N), range(1, N + 1))])
    B = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C) # Box number
        B[(r, c, n)] = [
            ("r_c", (r, c)),
            ("r_n", (r, n)),
            ("c_n", (c, n)),
            ("b_n", (b, n))]
    A, B = cover(A, B)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(A, B, (i, j, n))
    for solution in solve(A, B, []):
        for (r, c, n) in solution:
            grid[r][c] = n
        yield grid

def cover(A, B):
    A = {j: set() for j in A}
    for i, row in B.items():
        for j in row:
            A[j].add(i)
    return A, B

def solve(A, B, solution):
    if not A:
        yield list(solution)
    else:
        c = min(A, key=lambda c: len(A[c]))
        for r in list(A[c]):
            solution.append(r)
            cols = select(A, B, r)
            for s in solve(A, B, solution):
                yield s
            deselect(A, B, r, cols)
            solution.pop()

def select(A, B, r):
    cols = []
    for j in B[r]:
        for i in A[j]:
            for k in B[i]:
                if k != j:
                    A[k].remove(i)
        cols.append(A.pop(j))
    return cols

def deselect(A, B, r, cols):
    for j in reversed(B[r]):
        A[j] = cols.pop()
        for i in A[j]:
            for k in B[i]:
                if k != j:
                    A[k].add(i)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
