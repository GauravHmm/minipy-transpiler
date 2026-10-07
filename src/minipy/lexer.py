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

    LESS = auto()
    GREATER = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()

    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    COLON = auto()

    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()

    PRINT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    RANGE = auto()
    DEF = auto()
    RETURN = auto()

    AND = auto()
    OR = auto()
    NOT = auto()

    TRUE = auto()
    FALSE = auto()

    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str


class Lexer:
    keywords = {
        "print": TokenType.PRINT,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "for": TokenType.FOR,
        "in": TokenType.IN,
        "range": TokenType.RANGE,
        "def": TokenType.DEF,
        "return": TokenType.RETURN,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "not": TokenType.NOT,
        "True": TokenType.TRUE,
        "False": TokenType.FALSE,
    }

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.indent_levels = [0]
        self.at_line_start = True

    def tokenize(self) -> list[Token]:
        tokens = []

        while self.position < len(self.source):
            if self.at_line_start:
                self._handle_indentation(tokens)

                if self.position >= len(self.source):
                    break

            char = self.source[self.position]

            if char in " \t":
                self.position += 1
                continue

            if char == "#":
                self._skip_comment()
                continue

            if char == "\n":
                tokens.append(Token(TokenType.NEWLINE, "\\n"))
                self.position += 1
                self.at_line_start = True
                continue

            if char.isalpha() or char == "_":
                tokens.append(self._read_identifier())
                continue

            if char.isdigit():
                tokens.append(self._read_number())
                continue

            if char in "\"'":
                tokens.append(self._read_string())
                continue

            two_char_tokens = {
                "<=": TokenType.LESS_EQUAL,
                ">=": TokenType.GREATER_EQUAL,
                "==": TokenType.EQUAL,
                "!=": TokenType.NOT_EQUAL,
            }

            two_chars = self.source[self.position:self.position + 2]

            if two_chars in two_char_tokens:
                tokens.append(
                    Token(two_char_tokens[two_chars], two_chars)
                )
                self.position += 2
                continue

            token = {
                "=": TokenType.ASSIGN,
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.MULTIPLY,
                "/": TokenType.DIVIDE,
                "%": TokenType.MODULO,
                "<": TokenType.LESS,
                ">": TokenType.GREATER,
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                ",": TokenType.COMMA,
                ":": TokenType.COLON,
            }

            if char in token:
                tokens.append(Token(token[char], char))
                self.position += 1
                continue

            raise SyntaxError(f"Unexpected character: {char}")

        if not tokens or tokens[-1].type != TokenType.NEWLINE:
            tokens.append(Token(TokenType.NEWLINE, "\\n"))

        while len(self.indent_levels) > 1:
            self.indent_levels.pop()
            tokens.append(Token(TokenType.DEDENT, ""))

        tokens.append(Token(TokenType.EOF, ""))

        return tokens

    def _handle_indentation(self, tokens):
        start = self.position

        while (
            self.position < len(self.source)
            and self.source[self.position] in " \t"
        ):
            self.position += 1

        indentation = self.position - start

        # Blank line
        if (
            self.position < len(self.source)
            and self.source[self.position] == "\n"
        ):
            return

        # Comment-only line
        if (
            self.position < len(self.source)
            and self.source[self.position] == "#"
        ):
            return

        current_indent = self.indent_levels[-1]

        if indentation > current_indent:
            self.indent_levels.append(indentation)
            tokens.append(Token(TokenType.INDENT, ""))

        elif indentation < current_indent:
            while (
                len(self.indent_levels) > 1
                and indentation < self.indent_levels[-1]
            ):
                self.indent_levels.pop()
                tokens.append(Token(TokenType.DEDENT, ""))

            if indentation != self.indent_levels[-1]:
                raise SyntaxError("Invalid indentation")

        self.at_line_start = False

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

        if value in self.keywords:
            return Token(self.keywords[value], value)

        return Token(TokenType.IDENTIFIER, value)

    def _read_number(self) -> Token:
        start = self.position
        has_decimal = False

        while self.position < len(self.source):
            char = self.source[self.position]

            if char.isdigit():
                self.position += 1

            elif char == "." and not has_decimal:
                has_decimal = True
                self.position += 1

            else:
                break

        value = self.source[start:self.position]

        return Token(TokenType.NUMBER, value)

    def _read_string(self) -> Token:
        quote = self.source[self.position]
        self.position += 1

        start = self.position

        while (
            self.position < len(self.source)
            and self.source[self.position] != quote
        ):
            self.position += 1

        if self.position >= len(self.source):
            raise SyntaxError("Unterminated string")

        value = self.source[start:self.position]
        self.position += 1

        return Token(TokenType.STRING, value)

    def _skip_comment(self):
        while (
            self.position < len(self.source)
            and self.source[self.position] != "\n"
        ):
            self.position += 1