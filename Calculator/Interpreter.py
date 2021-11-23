from data_classes import NodeVisitor, BinOp
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

    @staticmethod
    def visit_Num(node):
        return node.value

    def interpret(self):
        return self.visit(self.tree)
