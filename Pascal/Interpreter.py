from data_classes import *
from Constants import *


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.GLOBAL_VARS = {}

    def visit_BinOp(self, node: BinOp):
        left = self.visit(node.left)
        right = self.visit(node.right)
        operator = node.token.type

        types = {
            PLUS: lambda x, y: x + y,
            MINUS: lambda x, y: x - y,
            MULT: lambda x, y: x * y,
            INTEGER_DIV: lambda x, y: x // y,
            FLOAT_DIV: lambda x, y: x / y,
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
    def visit_Num(node: Num):
        return node.value

    def visit_Compound(self, node: Compound):
        for sub_node in node.get_children():
            self.visit(sub_node)

    def visit_Assign(self, node: Assign):
        var_name = node.left.value
        expr = self.visit(node.right)
        self.GLOBAL_VARS[var_name] = expr

    def visit_Var(self, node: Var):
        var_name = node.value
        value = self.GLOBAL_VARS.get(var_name, None)
        if value is None:
            raise SyntaxError("variable '" + var_name + "' is not defined")
        return value

    def visit_NoOp(self, node):
        pass

    def visit_Program(self, node: Program):
        for declaration in node.var_decs:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecs(self, node: VarDecs):
        pass

    def interpret(self):
        return self.visit(self.tree)
