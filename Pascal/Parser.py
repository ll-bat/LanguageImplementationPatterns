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

    def program(self):
        node = self.compound_statement()
        self.match(DOT)
        return node

    def compound_statement(self):
        self.match(BEGIN)
        nodes = self.statement_list()
        self.match(END)

        compound = Compound()
        for node in nodes:
            compound.add(node)

        return compound

    def statement_list(self):
        children = [self.statement()]
        while self.lexer.get_current_token().type is SEMI:
            self.match(SEMI)
            nodes = self.statement_list()
            children += nodes
        return children

    def statement(self):
        token = self.lexer.get_current_token()
        if token.type is BEGIN:
            return self.compound_statement()
        elif token.type is ID:
            return self.assignment_statement()
        elif token.type is END:
            return self.emtpy()

        print(token)
        self.error("error in statement")

    def assignment_statement(self):
        var = self.variable()
        self.match(ASSIGN)
        expr = self.expr()
        return Assign(var, Token(ASSIGN, Assign), expr)

    @staticmethod
    def emtpy():
        return NoOp()

    def variable(self):
        token = self.lexer.get_current_token()
        if token.type is ID:
            self.lexer.go_forward()
            return Var(token)

        self.error("error in variable")

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
        elif token.type is ID:
            self.lexer.go_forward()
            return Var(token)
        else:
            self.error("incorrect expression: (from factor)")

    def parse(self):
        program = self.program()
        if self.lexer.is_pointer_out_of_text():
            # all characters consumed
            return program

        self.error("Syntax error at position " + self.lexer.get_position())
