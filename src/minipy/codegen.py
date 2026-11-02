
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


class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.declared_variables = set()
        self.variable_types = {}
        self.function_names = set()

    def indent(self):
        return "    " * self.indent_level

    def generate(self, statements):
        # Collect function names before generating calls.
        self.function_names = {
            statement.name
            for statement in statements
            if isinstance(statement, FunctionNode)
        }
        uses_input = any(
            self.statement_uses_input(statement)
            for statement in statements
        )

        lines = [
            "#include <iostream>",
            "#include <string>",
            "",
        ]

        if uses_input:
            lines.extend([
                "std::string minipy_input() {",
                "    std::string value;",
                "    std::getline(std::cin, value);",
                "    return value;",
                "}",
                "",
            ])

        # Generate functions before main().
        for statement in statements:
            if isinstance(statement, FunctionNode):
                lines.extend(self.generate_function(statement))
                lines.append("")

        lines.append("int main() {")
        self.indent_level = 1
        self.declared_variables = set()
        self.variable_types = {}

        for statement in statements:
            if not isinstance(statement, FunctionNode):
                lines.extend(self.generate_statement(statement))

        lines.append("    return 0;")
        lines.append("}")

        return "\n".join(lines) + "\n"

    def statement_uses_input(self, node):
        if isinstance(node, (AssignmentNode, PrintNode)):
            return self.expression_uses_input(node.expression)

        if isinstance(node, (IfNode, WhileNode)):
            return (
                self.expression_uses_input(node.condition)
                or any(
                    self.statement_uses_input(statement)
                    for statement in node.body
                )
                or any(
                    self.statement_uses_input(statement)
                    for statement in (node.else_body or [])
                )
            )

        if isinstance(node, ForNode):
            return (
                self.expression_uses_input(node.iterable)
                or any(
                    self.statement_uses_input(statement)
                    for statement in node.body
                )
            )

        if isinstance(node, FunctionNode):
            return any(
                self.statement_uses_input(statement)
                for statement in node.body
            )

        if isinstance(node, ReturnNode) and node.expression is not None:
            return self.expression_uses_input(node.expression)

        return False

    def expression_uses_input(self, node):
        if isinstance(node, CallNode):
            return (
                node.name == "input"
                or any(
                    self.expression_uses_input(argument)
                    for argument in node.arguments
                )
            )

        if isinstance(node, BinaryOpNode):
            return (
                self.expression_uses_input(node.left)
                or self.expression_uses_input(node.right)
            )

        if isinstance(node, UnaryOpNode):
            return self.expression_uses_input(node.operand)

        return False

    def generate_function(self, node):
        previous_indent = self.indent_level
        previous_variables = self.declared_variables
        previous_types = self.variable_types

        # Initially use int as the return type.
        parameters = ", ".join(
            f"int {parameter}" for parameter in node.parameters
        )

        lines = [
            f"int {node.name}({parameters}) {{"
        ]

        self.indent_level = 1
        self.declared_variables = set(node.parameters)
        self.variable_types = {parameter: "int" for parameter in node.parameters}

        for statement in node.body:
            lines.extend(self.generate_statement(statement))

        lines.append(self.indent() + "return 0;")
        lines.append("}")

        self.indent_level = previous_indent
        self.declared_variables = previous_variables
        self.variable_types = previous_types

        return lines

    def generate_statement(self, node):
        prefix = self.indent()

        if isinstance(node, AssignmentNode):
            expression = self.generate_expression(node.expression)

            if node.name not in self.declared_variables:
                variable_type = self.infer_type(node.expression)
                self.declared_variables.add(node.name)
                self.variable_types[node.name] = variable_type

                return [
                    f"{prefix}{variable_type} {node.name} = "
                    f"{expression};"
                ]

            return [f"{prefix}{node.name} = {expression};"]

        if isinstance(node, PrintNode):
            expression = self.generate_expression(node.expression)

            return [
                f"{prefix}std::cout << {expression} "
                f"<< std::endl;"
            ]

        if isinstance(node, IfNode):
            condition = self.generate_expression(node.condition)
            lines = [f"{prefix}if ({condition}) {{"]

            lines.extend(self.generate_block(node.body))
            lines.append(prefix + "}")

            if node.else_body is not None:
                lines[-1] += " else {"
                lines.extend(self.generate_block(node.else_body))
                lines.append(prefix + "}")

            return lines

        if isinstance(node, WhileNode):
            condition = self.generate_expression(node.condition)
            lines = [f"{prefix}while ({condition}) {{"]

            lines.extend(self.generate_block(node.body))
            lines.append(prefix + "}")

            return lines

        if isinstance(node, ForNode):
            if not (
                isinstance(node.iterable, CallNode)
                and node.iterable.name == "range"
            ):
                raise ValueError("Only range() loops are supported")

            arguments = [
                self.generate_expression(arg)
                for arg in node.iterable.arguments
            ]

            if len(arguments) == 1:
                start, stop, step = "0", arguments[0], "1"
            elif len(arguments) == 2:
                start, stop = arguments
                step = "1"
            elif len(arguments) == 3:
                start, stop, step = arguments
            else:
                raise ValueError(
                    "range() expects one, two, or three arguments"
                )

            lines = [
                f"{prefix}for (int {node.variable} = {start}; "
                f"{node.variable} < {stop}; "
                f"{node.variable} += {step}) {{"
            ]

            lines.extend(
                self.generate_block(node.body, {node.variable: "int"})
            )
            lines.append(prefix + "}")

            return lines

        if isinstance(node, ReturnNode):
            if node.expression is None:
                return [f"{prefix}return 0;"]

            expression = self.generate_expression(node.expression)
            return [f"{prefix}return {expression};"]

        raise ValueError(
            f"Unsupported statement: {type(node).__name__}"
        )

    def generate_block(self, statements, extra_types=None):
        """Generate a C++ block and keep block-local declarations local."""
        previous_variables = self.declared_variables.copy()
        previous_types = self.variable_types.copy()
        if extra_types:
            self.declared_variables.update(extra_types)
            self.variable_types.update(extra_types)

        self.indent_level += 1
        lines = []
        for statement in statements:
            lines.extend(self.generate_statement(statement))
        self.indent_level -= 1

        self.declared_variables = previous_variables
        self.variable_types = previous_types
        return lines

    def generate_expression(self, node):
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, StringNode):
            escaped = (
                node.value
                .replace("\\", "\\\\")
                .replace('"', '\\"')
                .replace("\n", "\\n")
                .replace("\t", "\\t")
            )
            return f'"{escaped}"'

        if isinstance(node, BooleanNode):
            return "true" if node.value else "false"

        if isinstance(node, IdentifierNode):
            return node.name

        if isinstance(node, BinaryOpNode):
            left = self.generate_expression(node.left)
            right = self.generate_expression(node.right)

            operators = {
                "and": "&&",
                "or": "||",
                "==": "==",
                "!=": "!=",
                "<": "<",
                ">": ">",
                "<=": "<=",
                ">=": ">=",
                "+": "+",
                "-": "-",
                "*": "*",
                "/": "/",
                "%": "%",
            }

            operator = operators.get(node.operator)

            if operator is None:
                raise ValueError(
                    f"Unsupported operator: {node.operator}"
                )

            if node.operator == "/":
                return f"(static_cast<double>({left}) / {right})"

            return f"({left} {operator} {right})"

        if isinstance(node, UnaryOpNode):
            operand = self.generate_expression(node.operand)

            if node.operator == "not":
                return f"(!{operand})"

            return f"({node.operator}{operand})"

        if isinstance(node, CallNode):
            if node.name == "input":
                return "minipy_input()"

            arguments = ", ".join(
                self.generate_expression(arg)
                for arg in node.arguments
            )

            return f"{node.name}({arguments})"

        raise ValueError(
            f"Unsupported expression: {type(node).__name__}"
        )

    def infer_type(self, node):
        if isinstance(node, StringNode):
            return "std::string"

        if isinstance(node, BooleanNode):
            return "bool"

        if isinstance(node, NumberNode):
            if "." in node.value:
                return "double"
            return "int"

        if isinstance(node, IdentifierNode):
            return self.variable_types.get(node.name, "int")

        if isinstance(node, BinaryOpNode):
            if node.operator in (
                "<", ">", "<=", ">=", "==", "!=", "and", "or"
            ):
                return "bool"

            left_type = self.infer_type(node.left)
            right_type = self.infer_type(node.right)

            if "std::string" in (left_type, right_type):
                return "std::string"

            if node.operator == "/":
                return "double"

            if "double" in (left_type, right_type):
                return "double"

            return "int"

        if isinstance(node, UnaryOpNode):
            if node.operator == "not":
                return "bool"
            return self.infer_type(node.operand)

        if isinstance(node, CallNode):
            if node.name == "input":
                return "std::string"

            if node.name == "range":
                return "int"

            return "int"

        # Variables require semantic type information for reliable
        # inference. Use int as a temporary default.
        return "int"
