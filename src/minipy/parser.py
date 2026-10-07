from minipy.lexer import TokenType
from minipy.ast import (
    NumberNode,
    IdentifierNode,
    BinaryOpNode,
    AssignmentNode,
    PrintNode,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position]

    def eat(self, token_type):
        token = self.current_token()

        if token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type}, got {token.type}"
            )

        self.position += 1
        return token

    def parse(self):
        statements = []

        while self.current_token().type != TokenType.EOF:
            statements.append(self.statement())

        return statements

    def statement(self):
        if self.current_token().type == TokenType.IDENTIFIER:
            return self.assignment()

        if self.current_token().type == TokenType.PRINT:
            return self.print_statement()

        raise SyntaxError(
            f"Unexpected token: {self.current_token().type}"
        )

    def assignment(self):
        name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.ASSIGN)

        expression = self.expression()

        return AssignmentNode(name, expression)

    def print_statement(self):
        self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)

        expression = self.expression()

        self.eat(TokenType.RPAREN)

        return PrintNode(expression)

    def expression(self):
        node = self.term()

        while self.current_token().type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            operator = self.current_token().value
            self.position += 1

            right = self.term()
            node = BinaryOpNode(node, operator, right)

        return node

    def term(self):
        node = self.factor()

        while self.current_token().type in (
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
            TokenType.MODULO,
        ):
            operator = self.current_token().value
            self.position += 1

            right = self.factor()
            node = BinaryOpNode(node, operator, right)

        return node

    def factor(self):
        token = self.current_token()

        if token.type == TokenType.NUMBER:
            self.position += 1
            return NumberNode(token.value)

        if token.type == TokenType.IDENTIFIER:
            self.position += 1
            return IdentifierNode(token.value)

        if token.type == TokenType.LPAREN:
            self.position += 1

            node = self.expression()

            self.eat(TokenType.RPAREN)

            return node

        raise SyntaxError(
            f"Unexpected token: {token.type}"
        )