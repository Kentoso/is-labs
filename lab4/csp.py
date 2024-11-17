from collections import defaultdict


class Constraint:
    def __init__(self, variables, is_satisfied):
        self.variables = variables
        self.is_satisfied = is_satisfied

    def check(self, assignment):
        if all(var in assignment for var in self.variables):
            return self.is_satisfied(assignment)
        return True


class CSP:
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains = domains
        self.constraints = defaultdict(list)

    def add_constraint(self, constraint):
        for variable in constraint.variables:
            self.constraints[variable].append(constraint)

    def is_consistent(self, variable, value, assignment):
        assignment[variable] = value
        for constraint in self.constraints[variable]:
            if not constraint.check(assignment):
                del assignment[variable]
                return False
        del assignment[variable]
        return True

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [v for v in self.variables if v not in assignment]
        return min(unassigned_vars, key=lambda var: len(self.domains[var]))

    def order_domain_values(self, var, assignment):
        return sorted(
            self.domains[var],
            key=lambda value: self.count_conflicts(var, value, assignment),
        )

    def count_conflicts(self, var, value, assignment):
        count = 0
        assignment[var] = value
        for constraint in self.constraints[var]:
            if not constraint.check(assignment):
                count += 1
        del assignment[var]
        return count

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result:
                    return result
                assignment.pop(var)

        return None


variables = ["X1", "X2", "X3"]
domains = {"X1": [1, 2, 3], "X2": [1, 2, 3], "X3": [1, 2, 3]}


csp = CSP(variables, domains)
csp.add_constraint(Constraint(["X1", "X2"], lambda a: a["X1"] > a["X2"]))
csp.add_constraint(Constraint(["X2", "X3"], lambda a: a["X2"] < a["X3"]))
csp.add_constraint(Constraint(["X1", "X3"], lambda a: a["X1"] < a["X3"]))


solution = csp.backtrack({})
print("Solution:", solution)
