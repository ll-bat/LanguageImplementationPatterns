from Parser import Parser
from Interpreter import Interpreter
from Constants import *
from Lexer import Lexer

try:
    string = """
        BEGIN
            BEGIN
                number := 2;
                a := number;
                b := 10 * a + 10 * number / 4;
                c := a - - b
            END;
            x := 11;
        END.
    """

    parser = Parser(string)
    tree = parser.parse()
    interpreter = Interpreter(tree)
    value = interpreter.interpret()
    print(value)
except SyntaxError as ex:
    print(ex.msg)
