
from minipy.lexer import TokenType
from minipy.ast import (
    NumberNode,
    StringNode,
    BooleanNode,
    IdentifierNode,
    BinaryOpNode,
    UnaryOpNode,
    AssignmentNode,
    PrintNode,
    IfNode,
    WhileNode,
    ForNode,
    FunctionNode,
    ReturnNode,
    CallNode,
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
                f"Expected {token_type.name}, "
                f"got {token.type.name} ('{token.value}')"
            )

        self.position += 1
        return token

    def parse(self):
        statements = []

        while self.current_token().type != TokenType.EOF:
            if self.current_token().type == TokenType.NEWLINE:
                self.eat(TokenType.NEWLINE)
                continue

            statements.append(self.statement())

        return statements

    # -------------------------
    # Statements
    # -------------------------

    def statement(self):
        token_type = self.current_token().type

        if token_type == TokenType.IDENTIFIER:
            return self.assignment()

        if token_type == TokenType.PRINT:
            return self.print_statement()

        if token_type == TokenType.IF:
            return self.if_statement()

        if token_type == TokenType.WHILE:
            return self.while_statement()

        if token_type == TokenType.FOR:
            return self.for_statement()

        if token_type == TokenType.DEF:
            return self.function_definition()

        if token_type == TokenType.RETURN:
            return self.return_statement()

        token = self.current_token()
        raise SyntaxError(
            f"Unexpected token: {token.type.name} ('{token.value}')"
        )

    def assignment(self):
        name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.ASSIGN)

        expression = self.expression()
        self.eat(TokenType.NEWLINE)

        return AssignmentNode(name, expression)

    def print_statement(self):
        self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)

        expression = self.expression()

        self.eat(TokenType.RPAREN)
        self.eat(TokenType.NEWLINE)

        return PrintNode(expression)

    def if_statement(self):
        self.eat(TokenType.IF)

        condition = self.expression()

        self.eat(TokenType.COLON)
        self.eat(TokenType.NEWLINE)
        self.eat(TokenType.INDENT)

        body = self.block()
        self.eat(TokenType.DEDENT)

        else_body = None

        if self.current_token().type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.COLON)
            self.eat(TokenType.NEWLINE)
            self.eat(TokenType.INDENT)

            else_body = self.block()
            self.eat(TokenType.DEDENT)

        return IfNode(condition, body, else_body)

    def while_statement(self):
        self.eat(TokenType.WHILE)

        condition = self.expression()

        self.eat(TokenType.COLON)
        self.eat(TokenType.NEWLINE)
        self.eat(TokenType.INDENT)

        body = self.block()
        self.eat(TokenType.DEDENT)

        return WhileNode(condition, body)

    def for_statement(self):
        self.eat(TokenType.FOR)

        variable = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.IN)

        iterable = self.expression()

        self.eat(TokenType.COLON)
        self.eat(TokenType.NEWLINE)
        self.eat(TokenType.INDENT)

        body = self.block()
        self.eat(TokenType.DEDENT)

        return ForNode(variable, iterable, body)

    def function_definition(self):
        self.eat(TokenType.DEF)

        name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.LPAREN)

        parameters = []

        if self.current_token().type != TokenType.RPAREN:
            parameters.append(
                self.eat(TokenType.IDENTIFIER).value
            )

            while self.current_token().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                parameters.append(
                    self.eat(TokenType.IDENTIFIER).value
                )

        self.eat(TokenType.RPAREN)
        self.eat(TokenType.COLON)
        self.eat(TokenType.NEWLINE)
        self.eat(TokenType.INDENT)

        body = self.block()
        self.eat(TokenType.DEDENT)

        return FunctionNode(name, parameters, body)

    def return_statement(self):
        self.eat(TokenType.RETURN)

        if self.current_token().type == TokenType.NEWLINE:
            self.eat(TokenType.NEWLINE)
            return ReturnNode(None)

        expression = self.expression()
        self.eat(TokenType.NEWLINE)

        return ReturnNode(expression)

    def block(self):
        statements = []

        while self.current_token().type not in (
            TokenType.DEDENT,
            TokenType.EOF,
        ):
            if self.current_token().type == TokenType.NEWLINE:
                self.eat(TokenType.NEWLINE)
            else:
                statements.append(self.statement())

        return statements

    # -------------------------
    # Expressions
    # -------------------------

    def expression(self):
        return self.logical_or()

    def logical_or(self):
        node = self.logical_and()

        while self.current_token().type == TokenType.OR:
            operator = self.eat(TokenType.OR).value
            right = self.logical_and()

            node = BinaryOpNode(node, operator, right)

        return node

    def logical_and(self):
        node = self.comparison()

        while self.current_token().type == TokenType.AND:
            operator = self.eat(TokenType.AND).value
            right = self.comparison()

            node = BinaryOpNode(node, operator, right)

        return node

    def comparison(self):
        node = self.arithmetic_expression()

        comparison_tokens = (
            TokenType.LESS,
            TokenType.GREATER,
            TokenType.LESS_EQUAL,
            TokenType.GREATER_EQUAL,
            TokenType.EQUAL,
            TokenType.NOT_EQUAL,
        )

        while self.current_token().type in comparison_tokens:
            operator = self.current_token().value
            self.position += 1

            right = self.arithmetic_expression()
            node = BinaryOpNode(node, operator, right)

        return node

    def arithmetic_expression(self):
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
        return self.unary()

    def unary(self):
        if self.current_token().type in (
            TokenType.MINUS,
            TokenType.NOT,
        ):
            operator = self.current_token().value
            self.position += 1

            operand = self.unary()
            return UnaryOpNode(operator, operand)

        return self.primary()

    def primary(self):
        token = self.current_token()

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberNode(token.value)

        if token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return StringNode(token.value)

        if token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return BooleanNode(True)

        if token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return BooleanNode(False)

        if token.type == TokenType.IDENTIFIER:
            name = self.eat(TokenType.IDENTIFIER).value

            if self.current_token().type == TokenType.LPAREN:
                return self.call(name)

            return IdentifierNode(name)

        if token.type == TokenType.RANGE:
            self.eat(TokenType.RANGE)
            return self.call("range")

        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)

            node = self.expression()

            self.eat(TokenType.RPAREN)
            return node

        raise SyntaxError(
            f"Unexpected token in expression: "
            f"{token.type.name} ('{token.value}')"
        )

    def call(self, name):
        self.eat(TokenType.LPAREN)

        arguments = []

        if self.current_token().type != TokenType.RPAREN:
            arguments.append(self.expression())

            while self.current_token().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                arguments.append(self.expression())

        self.eat(TokenType.RPAREN)

        return CallNode(name, arguments)
