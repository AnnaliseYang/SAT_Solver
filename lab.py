"""
6.101 Lab:
SAT Solver
"""

#!/usr/bin/env python3

import sys
import typing

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS


def transform_formula(formula):
    new_formula = []
    for clause in formula:
        new_clause = set(tuple(literal) for literal in clause)
        new_formula.append(new_clause)
    return new_formula


def update_formula(formula, assignment):
    """
    Updates a formula based on an assignment
    """
    new_formula = []
    for clause in formula:
        new_clause = set()
        if assignment not in clause:
            # check if variable exists in clause
            for literal in clause:
                if literal[0] == assignment[0]:
                    continue
                new_clause.add(literal)
            new_formula.append(new_clause)
    return new_formula


def update_formula_unit(formula):
    """
    Returns the updated formula after removing unit clauses
    """
    unit_clauses = set()
    unit_assignments = {}

    for clause in formula:  # find all unit clauses
        if len(clause) == 1:  # unit clause
            literal = list(clause)[0]

            if negate(literal) in unit_clauses:  # unsatisfiable
                return None, None

            var, value = literal
            unit_clauses.update(clause)
            unit_assignments[var] = value

    if not unit_clauses:
        return formula, {}

    new_formula = []

    for clause in formula:
        if clause.isdisjoint(unit_clauses):
            # clause does not contain already set True literals
            new_clause = set()
            for literal in clause:
                if negate(literal) not in unit_clauses:
                    # add literal to the clause
                    new_clause.add(literal)
            new_formula.append(new_clause)

    return new_formula, unit_assignments


def get_literals(formula):
    literals = set()
    for clause in formula:
        literals |= clause
    return literals


def negate(literal):
    return (literal[0], not literal[1])


def find_sat_assignment(formula, so_far=None, assigned=None):
    """Find an assignment that satisfies the given CNF formula"""
    if formula == []:  # True
        return {}
    if set() in formula:
        return None
    if so_far is None:
        so_far = set()
    if assigned is None:
        assigned = {}

    clause = min(formula, key=len)

    if clause:
        for literal in clause:
            if len(literal) != 2:
                return None
            var, value = literal

            # try assignment
            rest_formula = update_formula(formula, literal)
            all_visited = so_far | {tuple(literal)}

            rest_assignments = find_sat_assignment(rest_formula, all_visited)

            if rest_assignments is not None:
                return {var: value} | rest_assignments


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    if formula == []:  # True
        return {}
    if [] in formula:
        return None

    formula = transform_formula(formula)
    out = {}

    new_formula, unit_assignments = update_formula_unit(formula)

    while unit_assignments and new_formula is not None:
        out |= unit_assignments
        new_formula, unit_assignments = update_formula_unit(new_formula)

    if new_formula is not None:
        rest_assignments = find_sat_assignment(new_formula)
        if rest_assignments is not None:
            out |= rest_assignments
        return out if out else None


def only_desired_rooms(student_preferences):
    formula = []
    for student, preferred_rooms in student_preferences.items():
        clause = [(student + "_" + room, True) for room in preferred_rooms]
        formula.append(clause)
    return formula


def exactly_one_room(students, rooms):
    formula = []
    for student in students:
        for r1 in rooms:
            for r2 in rooms:
                if r1 != r2:
                    clause = [(student + "_" + r1, False), (student + "_" + r2, False)]
                    formula.append(clause)
    return formula


def combine_students(students, n):
    """returns a combination of n students from a list of students"""
    if n == 1:
        return [{s} for s in students]
    elif n <= len(students) / 2:
        out = []
        visited = set()
        for student in students:
            visited.add(student)
            sub_results = combine_students(students - visited, n - 1)
            for result in sub_results:
                group = result | {student}
                if group not in out:
                    out.append(group)
        return out
    else:
        reverse_results = combine_students(students, len(students) - n)
        return [students - result for result in reverse_results]
    # return combinations


# print(combine_students({1, 2, 3, 4, 5}, 3))


def capacity_constraint(students, room_capacities):
    formula = []
    for room, capacity in room_capacities.items():
        if capacity >= len(students):
            continue
        combination = combine_students(students, capacity + 1)
        for set_students in combination:
            formula.append([(student + "_" + room, False) for student in set_students])
    return formula


def boolify_scheduling_problem(student_preferences, room_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of room names (strings) that work for that student

    room_capacities: a dictionary mapping each room name to a positive integer
                     for how many students can fit in that room

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up

    We assume no student or room names contain underscores.
    """

    students = set(student_preferences.keys())
    rooms = set(room_capacities.keys())

    formula = (
        only_desired_rooms(student_preferences)
        + exactly_one_room(students, rooms)
        + capacity_constraint(students, room_capacities)
    )

    return formula


if __name__ == "__main__":
    import doctest

    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
