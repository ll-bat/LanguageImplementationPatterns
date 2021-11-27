from Lexer import Lexer
from Constants import *
from data_classes import *


class Parser:
    """
    --------- GRAMMAR ---------------
    program: PROGRAM variable SEMI block DOT
    block: declarations compound_statement
    declarations: VAR (variable_declaration SEMI)+ | (PROCEDURE ID SEMI block SEMI  )* | empty
    variable_declaration: ID (COMMA, ID)* COLON integer_type
    integer_type: INTEGER | REAL
    compound_statement: BEGIN statement_list END
    statement_list: statement (SEMI statement)*
    statement: assignment_statement | compound_statement | empty
    empty:
    assignment_statement: variable ASSIGN expr
    expr: term ((PLUS, MINUS) term)*
    term: factor ((DIV, MULT, FLOAT_DIV) factor)*
    factor: PLUS factor | MINUS factor | INTEGER | REAL_INTEGER | LPARENT expr RPARENT | variable
    variable: ID
    """

    def __init__(self, text):
        self.lexer = Lexer(text)

    def program(self):
        self.match(PROGRAM)
        self.variable()
        self.match(SEMI)
        program = self.block()
        self.match(DOT)
        return program

    def block(self):
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        return Program(declarations, compound_statement)

    def declarations(self) -> list:
        declarations = []
        if self.lexer.get_current_token().type is VAR:
            self.match(VAR)
            while self.lexer.get_current_token().type is ID:
                declarations.append(self.variable_declaration())
                self.match(SEMI)

        while self.lexer.get_current_token().type is PROCEDURE:
            self.match(PROCEDURE)
            proc_name = self.lexer.get_current_token().value
            self.match(ID)
            self.match(SEMI)
            block = self.block()
            self.match(SEMI)
            declarations.append(ProcedureDecl(proc_name, block))

        return declarations

    def variable_declaration(self):
        variables = []
        if self.lexer.get_current_token().type is not ID:
            self.error('should be ID, got: ' + self.lexer.get_current_token().type)

        variables.append(self.lexer.get_current_token())
        self.lexer.go_forward()

        while self.lexer.get_current_token().type is COMMA:
            self.lexer.go_forward()
            var = self.lexer.get_current_token()
            if var.type is not ID:
                self.error('should be ID, got: ' + self.lexer.get_current_token().type)
            variables.append(var)
            self.lexer.go_forward()

        self.match(COLON)
        integer_type = self.integer_type()
        return VarDecs(variables, integer_type)

    def integer_type(self):
        token = self.lexer.get_current_token()
        if token.type in (INTEGER, REAL):
            self.lexer.go_forward()
            return token

        self.error('should be integer|real, got ' + token.type)

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
        while self.lexer.get_current_token().type in (MULT, FLOAT_DIV, INTEGER_DIV):
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
        elif token.type == FLOAT:
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
