from Lexer import Lexer
from Constants import *
from data_classes import *


# grammar
# expr: term ([+, -] term)* ;
# term: factor ([*, /] factor)* ;
# factor: (+, -)factor | NUM | ('(' + expr + ')')* ;
class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)

    def error(self, message):
        raise SyntaxError(message)

    def match(self, token_type: str):
        token = self.lexer.get_current_token()
        if token.type is not token_type:
            print('-----------------------')
            print(token)
            print('should be: ' + token_type)
            print('-----------------------')
            self.error("incorrect expression")
        self.lexer.go_forward()

    def expr(self):
        node = self.term()
        while self.lexer.get_current_token().type in (PLUS, MINUS):
            current_op_token = self.lexer.get_current_token()
            self.lexer.go_forward()
            node = BinOp(node, current_op_token, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.lexer.get_current_token().type in (MULT, DIV):
            current_op_token = self.lexer.get_current_token()
            self.lexer.go_forward()
            node = BinOp(node, current_op_token, self.factor())
        return node

    def factor(self):
        token = self.lexer.get_current_token()
        if token.type is PLUS:
            self.match(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type is MINUS:
            self.match(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.lexer.go_forward()
            return Num(token)
        elif token.type is LPARENT:
            self.match(LPARENT)
            node = self.expr()
            self.match(RPARENT)
            return node
        else:
            self.error("incorrect expression: (from factor)")

    def parse(self):
        expr = self.expr()
        if self.lexer.is_pointer_out_of_text():
            # all characters consumed
            return expr
        self.error("Syntax error at position " + self.lexer.get_position())
