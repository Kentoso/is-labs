from collections import defaultdict


class Constraint:
    def __init__(self, variables, is_satisfied):
        self.variables = variables
        self.is_satisfied = is_satisfied

    def check(self, assignment):
        if all(var in assignment for var in self.variables):
            return self.is_satisfied(assignment)
        return True

    def __repr__(self):
        return f"Constraint({self.variables}, {self.is_satisfied})"


class CSP:
    def __init__(self, variables, domains, intermediate_assignment_hook=None):
        self.variables = variables
        self.domains = domains
        self.constraints: dict[str, list[Constraint]] = defaultdict(list)
        self.intermediate_assignment_hook = intermediate_assignment_hook

    def _call_intermediate_assignment_hook(self, assignment):
        if self.intermediate_assignment_hook is not None:
            self.intermediate_assignment_hook(assignment)

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

    def remaining_values(self, assignment, unassigned_variable):
        remaining_values = [
            d
            for d in self.domains[unassigned_variable]
            if self.is_consistent(unassigned_variable, d, assignment)
        ]

        return remaining_values

    # with Minimum Remaining Values (MRV) heuristic
    def select_unassigned_variable(self, assignment):
        unassigned_vars = [v for v in self.variables if v not in assignment]
        print("------------")
        print("Unassigned Vars:", unassigned_vars)
        print(
            "Remaining Values:",
            [len(self.remaining_values(assignment, var)) for var in unassigned_vars],
        )
        return min(
            unassigned_vars, key=lambda var: len(self.remaining_values(assignment, var))
        )

    def get_related_unassigned_vars(self, var, assignment):
        unassigned_vars = [v for v in self.variables if v not in assignment]
        related_unassigned_vars = list(
            set(
                [
                    unassigned_var
                    for c in self.constraints[var]
                    for unassigned_var in unassigned_vars
                    if unassigned_var in c.variables and unassigned_var != var
                ]
            )
        )

        return related_unassigned_vars

    # with Least Constraining Value (LCV) heuristic
    def order_domain_values(self, var, assignment):
        related_unassigned_vars = self.get_related_unassigned_vars(var, assignment)

        restriction_scores = {
            value: self.restriction_score(
                var, value, assignment, related_unassigned_vars
            )
            for value in self.domains[var]
        }

        print(f"Restriction Scores for {var}:", restriction_scores)

        return sorted(
            self.domains[var],
            key=lambda value: restriction_scores[value],
        )

    def restriction_score(self, var, value, assignment, related_unassigned_vars):
        score = 0
        assignment[var] = value

        for v in related_unassigned_vars:
            score += len(self.domains[v]) - len(self.remaining_values(assignment, v))

        del assignment[var]
        return score

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                self._call_intermediate_assignment_hook(assignment)
                result = self.backtrack(assignment)
                if result:
                    return result
                assignment.pop(var)

        return None
