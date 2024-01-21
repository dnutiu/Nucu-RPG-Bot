import logging

import tatsu

from src.dice.semantics import DieSemantics

DIE_GRAMMAR = """
    @@grammar::Die
    @@whitespace :: None

    start = die:die $;

    die = [number_of_dies:number] die_type:die_type die_number:number [modifier:die_modifier];
    die_modifier = op:operator modifier:number;

    operator = '+' | '-';

    die_type = 'd' | 'zd';

    number = /[0-9]+/ ;
"""


class DieParser:
    """
    Parser for the die grammar defined above.
    """

    def __init__(self):
        self._parser = tatsu.compile(DIE_GRAMMAR)
        self._semantics = DieSemantics()
        self._logger = logging.getLogger("DieParser")

    def parse(self, expression: str) -> int:
        """
        Parses the die expression and returns the result.
        """
        try:
            clean_expression = "".join(expression.split())
            result = self._parser.parse(clean_expression, semantics=self._semantics)
            logging.debug(f"rolling die for {expression} -> result={result}")
            return result
        except tatsu.exceptions.FailedParse as e:
            message = f"Failed to roll {expression}: {str(e)}"
            self._logger.error(message)
            raise ValueError(message) from e
