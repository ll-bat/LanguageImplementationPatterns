class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __str__(self) -> str:
        return f'Token({self.type}, {self.value})'


class AST:
    pass


class Num(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return f'Num({self.token.type}, {self.value})'


class BinOp(AST):
    def __init__(self, left, op: Token, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return f'BinOp({self.left}, {self.op.type}, {self.right})'


class NodeVisitor(object):
    def visit(self, node):
        class_name = type(node).__name__
        method_name = 'visit_' + class_name
        method = getattr(self, method_name)
        return method(node)
