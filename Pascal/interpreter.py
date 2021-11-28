from typing import List

from symbol_table import SymbolTable
from data_classes import *
from constants import *


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.symbol_table = SymbolTable()

    def error(self, message):
        pass

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

        if self.symbol_table.is_defined(var_name):
            return self.symbol_table.assign(var_name, Symbol(var_name, expr))
        else:
            raise ValueError(f"value {var_name} is not defined")

    def visit_Var(self, node: Var):
        var_name = node.value

        symbol = self.symbol_table.lookup(var_name)
        if symbol is None:
            raise SyntaxError("variable '" + var_name + "' is not defined")
        return symbol.value

    def visit_NoOp(self, node):
        pass

    def visit_Program(self, node: Program):
        nested_symbol_table = SymbolTable(enclosed_parent=None)
        self.symbol_table = nested_symbol_table

        self.visit(node.block)

        self.symbol_table = self.symbol_table.enclosed_parent

    def visit_Block(self, node: Block):
        for declaration in node.var_decs:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecs(self, node: VarDecs):
        declarations = node.get_declarations()
        symbol_type = node.get_type()
        # print(symbol_type)
        for var in declarations:
            symbol = VarSymbol(var.value, symbol_type.value)
            self.symbol_table.define(symbol)

    def visit_VarSymbol(self, node: VarSymbol):
        self.symbol_table.define(node)

    def visit_ProcedureDecl(self, node: ProcedureDecl):
        self.symbol_table.define(node)

    def visit_ProcedureCall(self, node: ProcedureCall):
        procedure: ProcedureDecl = self.symbol_table.lookup(node.name)
        parameter_names: List[Symbol] = procedure.params
        parameter_values = node.actual_params
        params = {}
        for var, val in zip(parameter_names, parameter_values):
            params[var.name] = self.visit(val)

        # self.define_new_scope()
        for param, item in params.items():
            print(param, item)

    def interpret(self):
        return self.visit(self.tree)
