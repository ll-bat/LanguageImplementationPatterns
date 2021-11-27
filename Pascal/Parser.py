from Lexer import Lexer
from Constants import *
from DataClasses import *


class Parser:
    """
    --------- GRAMMAR ---------------
    program: PROGRAM variable SEMI block DOT
    block: declarations compound_statement
    declarations: VAR (variable_declaration SEMI)+ | PROCEDURE ID (LPARENT formal_parameter_list RPARENT)? SEMI block SEMI | empty
    formal_parameter_list: formal_parameter (SEMI format_parameter)*
    format_parameter: ID (COMMA ID)* COLON integer_type
    variable_declaration: ID (COMMA, ID)* COLON integer_type
    integer_type: INTEGER | REAL
    compound_statement: BEGIN statement_list END
    statement_list: statement (SEMI statement)*
    statement: assignment_statement | procedure_call | compound_statement | empty
    procedure_call: ID LPARENT (expr (COMMA expr)*)* RPARENT SEMI
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
        block = self.block()
        self.match(DOT)
        return Program(block)

    def block(self):
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        return Block(declarations, compound_statement)

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

            parameters_list = []
            if self.lexer.current_token.type is LPARENT:
                self.match(LPARENT)
                parameters_list = self.parameters_list()
                self.match(RPARENT)

            self.match(SEMI)
            block = self.block()
            self.match(SEMI)

            procedure_decl = ProcedureDecl(proc_name, parameters_list, block)
            declarations.append(procedure_decl)

        return declarations

    def parameters_list(self) -> list:
        """
        ( a , b : INTEGER; c : REAL )
        """

        declarations = []

        var = self.lexer.get_current_token().value
        declarations.append(var)
        self.match(ID)

        while self.lexer.get_current_token().type is COMMA:
            self.match(COMMA)
            var = self.lexer.get_current_token().value
            declarations.append(var)
            self.match(ID)

        self.match(COLON)
        integer_type = self.integer_type()
        declarations = list(map(lambda x: VarSymbol(x, integer_type.value), declarations))

        if self.lexer.get_current_token().type is not RPARENT:
            self.match(SEMI)
            declarations.extend(self.parameters_list())

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
            next_token = self.lexer.peek_next_token()
            if next_token.type is LPARENT:
                # procedure call
                return self.procedure_call()
            else:
                # assignment
                return self.assignment_statement()
        elif token.type is END:
            return self.emtpy()

        print(token)
        self.error("error in statement")

    def procedure_call(self):
        """
        procedure_call: ID LPARENT (expr (COMMA expr)*)* RPARENT
        """
        current_token = self.lexer.get_current_token()
        proc_name = self.lexer.get_current_token().value
        self.match(ID)
        self.match(LPARENT)
        if self.lexer.peek_next_token().type is RPARENT:
            self.lexer.go_forward()
            self.match(RPARENT)
            self.match(SEMI)
            # no parameters
            return ProcedureCall(proc_name, [], current_token)
        else:
            params = [self.expr()]
            while self.lexer.get_current_token().type is COMMA:
                self.match(COMMA)
                params.append(self.expr())
            self.match(RPARENT)
            self.match(SEMI)
            return ProcedureCall(proc_name, params, current_token)

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

        print(token)
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
