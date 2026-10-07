from dataclasses import dataclass

class ASTNode:
    pass

@dataclass
class NumberNode(ASTNode):
    value: str

@dataclass
class IdentifierNode(ASTNode):
    name: str

@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class AssignmentNode(ASTNode):
    name: str
    expression: ASTNode

@dataclass
class PrintNode(ASTNode):
    expression: ASTNode