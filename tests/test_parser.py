
from minipy.lexer import Lexer
from minipy.parser import Parser
from minipy.ast import (
    AssignmentNode,
    BinaryOpNode,
    PrintNode,
    CallNode,
)


def parse_source(source):
    tokens = Lexer(source).tokenize()
    parser = Parser(tokens)
    return parser.parse()


def test_assignment():
    program = parse_source("x = 10")

    assert len(program) == 1
    assert isinstance(program[0], AssignmentNode)
    assert program[0].name == "x"


def test_print_statement():
    program = parse_source("print(10)")

    assert len(program) == 1
    assert isinstance(program[0], PrintNode)


def test_operator_precedence():
    program = parse_source("x = 10 + 20 * 5")

    expression = program[0].expression

    assert isinstance(expression, BinaryOpNode)
    assert expression.operator == "+"
    assert isinstance(expression.right, BinaryOpNode)
    assert expression.right.operator == "*"


def test_parentheses():
    program = parse_source("x = (10 + 20) * 5")

    expression = program[0].expression

    assert isinstance(expression, BinaryOpNode)
    assert expression.operator == "*"
    assert isinstance(expression.left, BinaryOpNode)
    assert expression.left.operator == "+"


def test_function_call():
    program = parse_source("x = range(5)")

    expression = program[0].expression

    assert isinstance(expression, CallNode)
    assert expression.name == "range"
    assert len(expression.arguments) == 1
