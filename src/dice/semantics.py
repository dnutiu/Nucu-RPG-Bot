import copy
import random
from collections import deque
from tatsu.ast import AST


# noinspection PyMethodMayBeStatic
class DieSemantics:
    def number(self, ast):
        return int(ast)

    def start(self, ast):
        die = ast.get("die")
        if isinstance(die, dict):
            return {"total": die.get("result"), "dies": [die]}
        elif isinstance(die, list):
            return_value = {"total": 0, "dies": copy.deepcopy(die)}
            operators = ast.get("op", [])
            if not isinstance(operators, list):
                operators = [operators]
            operators = deque(operators)

            die_results = deque(map(lambda x: x.get("result"), die))
            # Note: we may need to use a dequeue, the ops are quite inefficient.
            while len(die_results) != 1:
                left = die_results.popleft()
                right = die_results.popleft()
                operator = operators.popleft()
                total = 0
                if operator == "+":
                    total = left + right
                if operator == "-":
                    total = left - right
                if operator == "adv":
                    total = max(left, right)
                if operator == "dis":
                    total = min(left, right)
                die_results.appendleft(total)

            return_value["total"] = die_results.pop()
            return return_value

    def die(self, ast):
        if not isinstance(ast, AST):
            return ast
        # the number of dies is optional; by default, we have one die
        number_of_dies = ast.get("number_of_dies") or 1

        die_type = ast.get("die_type")
        die_number = ast.get("die_number")

        # modifier is optional, if it doesn't exist we use 0
        die_modifier = ast.get("modifier") or 0

        minimum_value_for_die = 1
        if die_type == "zd":
            # zero-based die can output 0.
            minimum_value_for_die = 0

        rolls = [
            random.randint(minimum_value_for_die, die_number)
            for _ in range(number_of_dies)
        ]

        return {
            "result": max(sum(rolls) + die_modifier, minimum_value_for_die),
            "type": die_type,
            "rolls": rolls,
            "modifier": die_modifier,
        }

    def die_modifier(self, ast):
        if not isinstance(ast, AST):
            return ast
        op = ast.get("op")
        modifier = ast.get("modifier", 0)
        if op == "+":
            return modifier
        else:
            return -modifier
