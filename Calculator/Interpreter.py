from data_classes import NodeVisitor, BinOp, UnaryOp, Token
from Constants import *


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree

    def visit_BinOp(self, node: BinOp):
        left = self.visit(node.left)
        right = self.visit(node.right)
        operator = node.token.type

        types = {
            PLUS: lambda x, y: x + y,
            MINUS: lambda x, y: x - y,
            MULT: lambda x, y: x * y,
            DIV: lambda x, y: x / y,
        }

        return types[operator](left, right)

    def visit_UnaryOp(self, node: UnaryOp):
        op: Token = node.op
        expr = node.expr
        if op.type is PLUS:
            return +self.visit(expr)
        else:
            return -self.visit(expr)

    @staticmethod
    def visit_Num(node):
        return node.value

    def interpret(self):
        return self.visit(self.tree)
