
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


class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    def __init__(self):
        # Variables defined outside functions.
        self.variables = {}

        # Function name -> FunctionNode.
        self.functions = {}

        # Current function's local variables.
        self.local_variables = None

        # Used to detect return statements outside functions.
        self.inside_function = False

    def analyze(self, statements):
        # First collect function definitions so calls can refer
        # to functions defined later in the source.
        for statement in statements:
            if isinstance(statement, FunctionNode):
                if statement.name in self.functions:
                    raise SemanticError(
                        f"Function '{statement.name}' is already defined"
                    )

                self.functions[statement.name] = statement

        # Then analyze all statements.
        for statement in statements:
            self.check_statement(statement)

        return True

    # -------------------------
    # Statement checking
    # -------------------------

    def check_statement(self, node):
        if isinstance(node, AssignmentNode):
            value_type = self.check_expression(node.expression)

            if self.local_variables is not None:
                self.assign_variable(
                    self.local_variables, node.name, value_type
                )
            else:
                self.assign_variable(
                    self.variables, node.name, value_type
                )

        elif isinstance(node, PrintNode):
            self.check_expression(node.expression)

        elif isinstance(node, IfNode):
            condition_type = self.check_expression(node.condition)
            self.require_boolean(condition_type, "if condition")

            for statement in node.body:
                self.check_statement(statement)

            if node.else_body is not None:
                for statement in node.else_body:
                    self.check_statement(statement)

        elif isinstance(node, WhileNode):
            condition_type = self.check_expression(node.condition)
            self.require_boolean(condition_type, "while condition")

            for statement in node.body:
                self.check_statement(statement)

        elif isinstance(node, ForNode):
            if not (
                isinstance(node.iterable, CallNode)
                and node.iterable.name == "range"
            ):
                raise SemanticError(
                    "For loops must iterate over range()"
                )

            self.check_expression(node.iterable)

            if self.local_variables is not None:
                self.local_variables[node.variable] = "int"
            else:
                self.variables[node.variable] = "int"

            for statement in node.body:
                self.check_statement(statement)

        elif isinstance(node, FunctionNode):
            self.check_function(node)

        elif isinstance(node, ReturnNode):
            if not self.inside_function:
                raise SemanticError(
                    "'return' can only be used inside a function"
                )

            if node.expression is not None:
                self.check_expression(node.expression)

        else:
            raise SemanticError(
                f"Unsupported statement: {type(node).__name__}"
            )

    def check_function(self, function):
        # A function gets its own local variable dictionary.
        previous_locals = self.local_variables
        previous_function_state = self.inside_function

        self.local_variables = {}
        self.inside_function = True

        try:
            # Parameters are initially unknown because MiniPy
            # does not require parameter type annotations.
            for parameter in function.parameters:
                if parameter in self.local_variables:
                    raise SemanticError(
                        f"Duplicate parameter '{parameter}' "
                        f"in function '{function.name}'"
                    )

                self.local_variables[parameter] = "unknown"

            for statement in function.body:
                self.check_statement(statement)

        finally:
            # Restore the surrounding scope.
            self.local_variables = previous_locals
            self.inside_function = previous_function_state

    # -------------------------
    # Variable checking
    # -------------------------

    def assign_variable(self, scope, name, value_type):
        previous_type = scope.get(name)

        if previous_type is None:
            scope[name] = value_type
            return

        # An unknown type can be inferred from a later assignment.
        if previous_type == "unknown":
            scope[name] = value_type
            return

        if value_type == "unknown":
            return

        # Allow integers to be promoted to floats.
        if previous_type == "float" and value_type == "int":
            return

        if previous_type == "int" and value_type == "float":
            scope[name] = "float"
            return

        if previous_type != value_type:
            raise SemanticError(
                f"Cannot assign a {value_type} value to "
                f"variable '{name}' of type {previous_type}"
            )

    def get_variable_type(self, name):
        # Look in local variables first.
        if self.local_variables is not None:
            if name in self.local_variables:
                return self.local_variables[name]

        # Functions may read variables defined globally.
        if name in self.variables:
            return self.variables[name]

        raise SemanticError(
            f"Variable '{name}' is not defined"
        )

    # -------------------------
    # Expression checking
    # -------------------------

    def check_expression(self, node):
        if isinstance(node, NumberNode):
            if "." in node.value:
                return "float"

            return "int"

        if isinstance(node, StringNode):
            return "string"

        if isinstance(node, BooleanNode):
            return "bool"

        if isinstance(node, IdentifierNode):
            return self.get_variable_type(node.name)

        if isinstance(node, UnaryOpNode):
            operand_type = self.check_expression(node.operand)

            if node.operator == "-":
                if operand_type not in ("int", "float", "unknown"):
                    raise SemanticError(
                        "Unary minus requires a numeric value"
                    )

                return operand_type

            if node.operator == "not":
                self.require_boolean(operand_type, "'not' operator")
                return "bool"

        if isinstance(node, BinaryOpNode):
            left_type = self.check_expression(node.left)
            right_type = self.check_expression(node.right)

            operator = node.operator

            # Arithmetic operators.
            if operator in ("+", "-", "*", "/", "%"):
                return self.check_arithmetic(
                    operator, left_type, right_type
                )

            # Comparison operators.
            if operator in (
                "<", ">", "<=", ">=", "==", "!="
            ):
                return self.check_comparison(
                    operator, left_type, right_type
                )

            # Logical operators.
            if operator in ("and", "or"):
                self.require_boolean(left_type, operator)
                self.require_boolean(right_type, operator)
                return "bool"

        if isinstance(node, CallNode):
            return self.check_call(node)

        raise SemanticError(
            f"Unsupported expression: {type(node).__name__}"
        )

    def check_arithmetic(self, operator, left_type, right_type):
        # Permit unknown types when a function parameter's type
        # cannot yet be inferred.
        if "unknown" in (left_type, right_type):
            return "unknown"

        # String concatenation is supported with +.
        if operator == "+" and (
            left_type == "string" and right_type == "string"
        ):
            return "string"

        numeric_types = ("int", "float")

        if (
            left_type not in numeric_types
            or right_type not in numeric_types
        ):
            raise SemanticError(
                f"Operator '{operator}' requires numeric operands"
            )

        if operator == "/":
            return "float"

        if "float" in (left_type, right_type):
            return "float"

        return "int"

    def check_comparison(self, operator, left_type, right_type):
        if "unknown" in (left_type, right_type):
            return "bool"

        numeric_types = ("int", "float")

        if left_type in numeric_types and right_type in numeric_types:
            return "bool"

        if left_type == right_type:
            if operator in ("<", ">", "<=", ">="):
                if left_type == "string":
                    return "bool"

                raise SemanticError(
                    f"Operator '{operator}' cannot compare "
                    f"values of type {left_type}"
                )

            return "bool"

        raise SemanticError(
            f"Cannot compare {left_type} with {right_type}"
        )

    def require_boolean(self, value_type, context):
        if value_type not in ("bool", "unknown"):
            raise SemanticError(
                f"{context} must be a boolean expression"
            )

    # -------------------------
    # Function call checking
    # -------------------------

    def check_call(self, node):
        if node.name == "range":
            if not 1 <= len(node.arguments) <= 3:
                raise SemanticError(
                    "range() expects 1, 2, or 3 arguments"
                )

            for argument in node.arguments:
                argument_type = self.check_expression(argument)

                if argument_type not in ("int", "unknown"):
                    raise SemanticError(
                        "range() arguments must be integers"
                    )

            return "range"

        if node.name not in self.functions:
            raise SemanticError(
                f"Function '{node.name}' is not defined"
            )

        function = self.functions[node.name]

        if len(node.arguments) != len(function.parameters):
            raise SemanticError(
                f"Function '{node.name}' expects "
                f"{len(function.parameters)} arguments, "
                f"but got {len(node.arguments)}"
            )

        for argument in node.arguments:
            self.check_expression(argument)

        # Return-type inference will be added in a later version.
        return "unknown"
