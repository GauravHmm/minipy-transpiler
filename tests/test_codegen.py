
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
