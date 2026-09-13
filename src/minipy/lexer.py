from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()

    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()

    LPAREN = auto()
    RPAREN = auto()

    PRINT = auto()

    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0

    def tokenize(self) -> list[Token]:
        tokens = []

        while self.position < len(self.source):
            char = self.source[self.position]

            if char.isspace():
                self.position += 1
                continue

            if char.isalpha() or char == "_":
                tokens.append(self._read_identifier())
                continue

            if char.isdigit():
                tokens.append(self._read_number())
                continue

            token = {
                "=": TokenType.ASSIGN,
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.MULTIPLY,
                "/": TokenType.DIVIDE,
                "%": TokenType.MODULO,
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
            }

            if char in token:
                tokens.append(Token(token[char], char))
                self.position += 1
                continue

            raise SyntaxError(f"Unexpected character: {char}")

        tokens.append(Token(TokenType.EOF, ""))
        return tokens

    def _read_identifier(self) -> Token:
        start = self.position

        while (
            self.position < len(self.source)
            and (
                self.source[self.position].isalnum()
                or self.source[self.position] == "_"
            )
        ):
            self.position += 1

        value = self.source[start:self.position]

        if value == "print":
            return Token(TokenType.PRINT, value)

        return Token(TokenType.IDENTIFIER, value)

    def _read_number(self) -> Token:
        start = self.position

        while (
            self.position < len(self.source)
            and self.source[self.position].isdigit()
        ):
            self.position += 1

        value = self.source[start:self.position]

        return Token(TokenType.NUMBER, value)