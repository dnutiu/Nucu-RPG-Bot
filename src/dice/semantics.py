import random
from tatsu.ast import AST


# noinspection PyMethodMayBeStatic
class DieSemantics:
    def number(self, ast):
        return int(ast)

    def start(self, ast):
        modifier = ast.get("modifier") or 0
        die = ast.get("die")
        return die + modifier

    def die(self, ast):
        if not isinstance(ast, AST):
            return ast
        number_of_dies = ast.get("number_of_dies") or 1
        die_type = ast.get("die_type")
        die_number = ast.get("die_number") or 1
        if die_number <= 0:
            return 0
        # normal die
        if die_type == "d":
            return sum([random.randint(1, die_number) for _ in range(number_of_dies)])
        # zero-based die can output 0.
        if die_type == "zd":
            return sum([random.randint(0, die_number) for _ in range(number_of_dies)])
        raise ValueError(f"Invalid die type: {die_type}")

    def die_modifier(self, ast):
        if not isinstance(ast, AST):
            return ast
        op = ast.get("op")
        modifier = ast.get("modifier", 0)
        if op == "+":
            return modifier
        else:
            return -modifier
