import tatsu

from src.dice.semantics import DieSemantics

DIE_GRAMMAR = '''
    @@grammar::Die
    @@whitespace :: None

    start = [number_of_dies:number] die:die [modifier:die_modifier] $;
    die = die_type:die_type die_number:number;
    die_modifier = op:die_modifier_op modifier:number;
    die_modifier_op = '+' | '-';
    die_type = 'd' | 'zd';
    number = /[0-9]+/ ;
'''


class DieParser:
    """
        Parser for the die grammar defined above.
    """

    def __init__(self):
        self._parser = tatsu.compile(DIE_GRAMMAR)
        self._semantics = DieSemantics()

    def parse(self, expression: str) -> int:
        """
            Parses the die expression and returns the result.
        """
        clean_expression = "".join(expression.split())
        result = self._parser.parse(clean_expression, semantics=self._semantics)
        number_of_dies = result.get("number_of_dies") or 1
        modifier = result.get("modifier") or 0
        die = result.get("die")
        return number_of_dies * die + modifier
