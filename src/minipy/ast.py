from dataclasses import dataclass


class ASTNode:
    pass


@dataclass
class NumberNode(ASTNode):
    value: str


@dataclass
class StringNode(ASTNode):
    value: str


@dataclass
class BooleanNode(ASTNode):
    value: bool


@dataclass
class IdentifierNode(ASTNode):
    name: str


@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryOpNode(ASTNode):
    operator: str
    operand: ASTNode


@dataclass
class AssignmentNode(ASTNode):
    name: str
    expression: ASTNode


@dataclass
class PrintNode(ASTNode):
    expression: ASTNode


@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    body: list[ASTNode]
    else_body: list[ASTNode] | None = None


@dataclass
class WhileNode(ASTNode):
    condition: ASTNode
    body: list[ASTNode]


@dataclass
class ForNode(ASTNode):
    variable: str
    iterable: ASTNode
    body: list[ASTNode]


@dataclass
class FunctionNode(ASTNode):
    name: str
    parameters: list[str]
    body: list[ASTNode]


@dataclass
class ReturnNode(ASTNode):
    expression: ASTNode | None


@dataclass
class CallNode(ASTNode):
    name: str
    arguments: list[ASTNode]