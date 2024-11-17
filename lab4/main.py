from csp import CSP, Constraint
import copy


def add_row_constraints(csp):
    for row in range(1, 5):
        row_vars = [f"X{row}{col}" for col in range(1, 5)]
        for i in range(4):
            for j in range(i + 1, 4):
                csp.add_constraint(
                    Constraint(
                        [row_vars[i], row_vars[j]],
                        lambda assignment,
                        var1=row_vars[i],
                        var2=row_vars[j]: assignment[var1] != assignment[var2],
                    )
                )


def add_column_constraints(csp):
    for col in range(1, 5):
        col_vars = [f"X{row}{col}" for row in range(1, 5)]
        for i in range(4):
            for j in range(i + 1, 4):
                csp.add_constraint(
                    Constraint(
                        [col_vars[i], col_vars[j]],
                        lambda assignment,
                        var1=col_vars[i],
                        var2=col_vars[j]: assignment[var1] != assignment[var2],
                    )
                )


def add_subgrid_constraints(csp):
    subgrid_starts = [(1, 1), (1, 3), (3, 1), (3, 3)]
    for start_row, start_col in subgrid_starts:
        subgrid_vars = [
            f"X{start_row + i}{start_col + j}" for i in range(2) for j in range(2)
        ]
        for i in range(4):
            for j in range(i + 1, 4):
                csp.add_constraint(
                    Constraint(
                        [subgrid_vars[i], subgrid_vars[j]],
                        lambda assignment,
                        var1=subgrid_vars[i],
                        var2=subgrid_vars[j]: assignment[var1] != assignment[var2],
                    )
                )


variables = [f"X{i}{j}" for i in range(1, 5) for j in range(1, 5)]
domains = {var: [1, 2, 3, 4] for var in variables}


def print_sudoku_solution(solution):
    if not solution:
        print("No solution found.")
        return
    for row in range(1, 5):
        print(
            " ".join(
                str(solution[f"X{row}{col}"]) if f"X{row}{col}" in solution else "_"
                for col in range(1, 5)
            )
        )


csp = CSP(variables, domains, print_sudoku_solution)
add_row_constraints(csp)
add_column_constraints(csp)
add_subgrid_constraints(csp)

initial_map = [
    [0, 3, 0, 0],
    [4, 0, 0, 0],
    [0, 0, 3, 2],
    [0, 0, 0, 0],
]

initial_assignment = {
    f"X{row+1}{col+1}": initial_map[row][col]
    for row in range(4)
    for col in range(4)
    if initial_map[row][col] != 0
}

print("Initial Assignment:")
print_sudoku_solution(initial_assignment)

solution = csp.backtrack(initial_assignment)

print("Solution:")
print_sudoku_solution(solution)
