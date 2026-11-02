
import pytest

from minipy.lexer import Lexer
from minipy.parser import Parser
from minipy.semantic import SemanticAnalyzer, SemanticError


def analyze_source(source):
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()

    analyzer = SemanticAnalyzer()
    return analyzer.analyze(program)


def test_valid_assignment():
    source = """
x = 10
y = x + 20
print(y)
"""
    assert analyze_source(source) is True


def test_undefined_variable():
    source = "print(y)"

    with pytest.raises(SemanticError, match="not defined"):
        analyze_source(source)


def test_type_mismatch():
    source = """
x = 10
x = "hello"
"""

    with pytest.raises(SemanticError, match="Cannot assign"):
        analyze_source(source)


def test_undefined_function():
    source = "x = unknown_function(5)"

    with pytest.raises(SemanticError, match="not defined"):
        analyze_source(source)


def test_wrong_number_of_arguments():
    source = """
def add(a, b):
    return a + b

x = add(10)
"""

    with pytest.raises(SemanticError, match="expects"):
        analyze_source(source)


def test_duplicate_function_parameters():
    source = """
def add(a, a):
    return a
"""

    with pytest.raises(SemanticError, match="Duplicate parameter"):
        analyze_source(source)


def test_range_loop():
    source = """
for i in range(5):
    print(i)
"""

    assert analyze_source(source) is True


def test_invalid_if_condition():
    source = """
if 10:
    print(1)
"""

    with pytest.raises(SemanticError, match="boolean"):
        analyze_source(source)


def test_return_outside_function():
    source = "return 10"

    with pytest.raises(SemanticError, match="inside a function"):
        analyze_source(source)


def test_block_local_variable_cannot_be_used_after_if():
    source = """
if True:
    inside = 1
print(inside)
"""

    with pytest.raises(SemanticError, match="not defined"):
        analyze_source(source)


def test_functions_require_integer_arguments_and_returns():
    with pytest.raises(SemanticError, match="integer"):
        analyze_source("""
def identity(value):
    return value

result = identity("text")
""")

    with pytest.raises(SemanticError, match="return an integer"):
        analyze_source("""
def greeting():
    return "hello"
""")


def test_range_step_and_modulo_require_integers():
    with pytest.raises(SemanticError, match="positive integer"):
        analyze_source("""
for number in range(0, 5, -1):
    print(number)
""")

    with pytest.raises(SemanticError, match="integer operands"):
        analyze_source("result = 5.0 % 2")


def test_input_returns_a_string_and_rejects_arguments():
    assert analyze_source("name = input()\nprint(name)") is True

    with pytest.raises(SemanticError, match="does not accept arguments"):
        analyze_source('name = input("Name: ")')
