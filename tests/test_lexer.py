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

    assert tokens[5].type == TokenType.NEWLINE
    assert tokens[6].type == TokenType.EOF

def test_print_statement():
    tokens = Lexer("print(10)").tokenize()

    assert tokens[0].type == TokenType.PRINT
    assert tokens[1].type == TokenType.LPAREN
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[3].type == TokenType.RPAREN
    assert tokens[4].type == TokenType.NEWLINE
    assert tokens[5].type == TokenType.EOF


def test_keywords():
    tokens = Lexer("if True").tokenize()

    assert tokens[0].type == TokenType.IF
    assert tokens[1].type == TokenType.TRUE


def test_indentation():
    source = "if True:\n    print(10)"
    tokens = Lexer(source).tokenize()

    token_types = [token.type for token in tokens]

    assert TokenType.INDENT in token_types
    assert TokenType.DEDENT in token_types