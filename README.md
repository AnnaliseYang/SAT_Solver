# SAT Solver

This SAT Solver finds a satisfying assignment for a given CNF formula.

## Usage

To use the SAT solver, import the `satisfying_assignment` function and pass your CNF formula as input.

```python
from lab import satisfying_assignment

formula = [[('a', True), ('b', False)], [('c', True)]]
result = satisfying_assignment(formula)
print(result)
```

## CNF Representation

When representing problems in CNF (Conjunctive Normal Form), we use the following conventions:

- **Variable**: Represented as a Python string.
- **Literal**: A tuple containing a variable and a Boolean value (False if negated, True otherwise).
- **Clause**: A list of literals.
- **Formula**: A list of clauses.

For example, see the python representation of the following CNF formula:

```python
rule1 = [[('a', True), ('b', True), ('c', False)], [('c', True), ('d', True)]]
```

Which translates to
```python
(a or b or not c) and (c or d)
```

### Scheduling by Reduction:
Here we provided a helper function to convert an example scheduling problem into CNF.
- `boolify_scheduling_problem(student_preferences, room_capacities)`

Assignment clauses are made according to the following rules:

1. **Students' Preferences**: Students are only assigned to rooms included in their preferences.
2. **One Room per Student**: Each student is assigned to exactly one room.
3. **Room Capacity**: No room has more assigned students than it can fit.

## Example

```python
from lab import satisfying_assignment, boolify_scheduling_problem

student_preferences = {
    'Alice': {'Room1', 'Room2'},
    'Bob': {'Room2', 'Room3'},
    'Charlie': {'Room1'}
}

room_capacities = {
    'Room1': 1,
    'Room2': 2,
    'Room3': 1
}

formula = boolify_scheduling_problem(student_preferences, room_capacities)
assignment = satisfying_assignment(formula)
print(assignment)
```

For detailed instructions, please refer to the individual function docstrings.
