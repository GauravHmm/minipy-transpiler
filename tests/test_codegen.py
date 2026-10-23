
from minipy.lexer import Lexer
from minipy.parser import Parser
from minipy.semantic import SemanticAnalyzer
from minipy.codegen import CodeGenerator


def compile_minipy(source):
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()

    SemanticAnalyzer().analyze(program)

    return CodeGenerator().generate(program)


def test_assignment_and_print():
    output = compile_minipy(
        "x = 10\nprint(x)"
    )

    assert "int x = 10;" in output
    assert "std::cout << x << std::endl;" in output
    assert "int main()" in output


def test_arithmetic():
    output = compile_minipy(
        "x = 10 + 20 * 5"
    )

    assert "(10 + (20 * 5))" in output


def test_if_statement():
    output = compile_minipy(
        "x = 10\nif x > 5:\n    print(x)"
    )

    assert "if ((x > 5)) {" in output
    assert "std::cout << x << std::endl;" in output


def test_assignment_from_a_string_identifier_uses_string_type():
    output = compile_minipy('message = "hello"\ncopy = message')

    assert "std::string copy = message;" in output


def test_string_escaping_is_valid_cpp():
    output = compile_minipy('message = "say \\"hello\\"\\n"\nprint(message)')

    assert '"say \\"hello\\"\\n"' in output


def test_integer_function_call_is_generated():
    output = compile_minipy(
        "def add_one(value):\n"
        "    return value + 1\n"
        "result = add_one(4)\n"
        "print(result)"
    )

    assert "int add_one(int value)" in output
    assert "int result = add_one(4);" in output


def test_integer_division_uses_a_double_expression():
    output = compile_minipy("result = 5 / 2")

    assert "double result" in output
    assert "static_cast<double>(5) / 2" in output
