from Parser import Parser
from Interpreter import Interpreter
from Constants import *
from Lexer import Lexer

try:
    lexer = Lexer("BEGIN"
                  " "
                  "x := 2;"
                  "y := x + 2 * (x + 2);"
                  "END . ")

    while lexer.get_current_token().type is not EOF:
        token = lexer.get_current_token()
        print(token)
        lexer.get_next_token()

except SyntaxError as ex:
    print(ex.msg)
