import random
from tatsu.ast import AST


# noinspection PyMethodMayBeStatic
class DieSemantics:
    def number(self, ast):
        return int(ast)

    def die(self, ast):
        if not isinstance(ast, AST):
            return ast
        die_type = ast.get("die_type")
        die_number = ast.get("die_number", 1)
        if die_number <= 0:
            raise ValueError(f"Invalid die number: {die_number}")
        # normal die
        if die_type == "d":
            return random.randint(1, die_number)
        # zero-based die can output 0.
        if die_type == "zd":
            return random.randint(0, die_number)
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
