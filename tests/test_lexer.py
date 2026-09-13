from minipy.lexer import Lexer, TokenType


def test_simple_assignment():
    source = "x = 10 + 20"

    tokens = Lexer(source).tokenize()

    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "x"

    assert tokens[1].type == TokenType.ASSIGN

    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == "10"

    assert tokens[3].type == TokenType.PLUS

    assert tokens[4].type == TokenType.NUMBER
    assert tokens[4].value == "20"

    assert tokens[5].type == TokenType.EOF