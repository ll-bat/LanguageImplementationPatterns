from Parser import Parser
from Interpreter import Interpreter
from Constants import *
from Lexer import Lexer
from SemanticAnalyzer import SemanticAnalyzer

try:
    string = """
        PROGRAM Part10;
            VAR
               number     : INTEGER;
               a, b, c, x : INTEGER;
               y          : REAL;
            
            PROCEDURE p1 (a, b : INTEGER; z : REAL);
            VAR 
                y       : REAL;
            BEGIN
                c := z
            END;
            
            PROCEDURE p2;
            BEGIN
                
            END;
            
            BEGIN {Part10}
               BEGIN
                  number := 2;
                  a := number;
                  b := 10 * a + 10 * number DIV 4;
                  c := a - - b;
                  p1 (1 + 2, 3);
               END;
               x := 11;
               y := 20 / 7 + 3.14;
               { writeln('a = ', a); }
               { writeln('b = ', b); }
               { writeln('c = ', c); }
               { writeln('number = ', number); }
               { writeln('x = ', x); }
               { writeln('y = ', y); }
            END.  {Part10}
    """

    # lexer = Lexer(string)
    # while lexer.get_current_token().type is not EOF:
    #     print(lexer.get_current_token())
    #     lexer.go_forward()

    parser = Parser(string)
    tree = parser.parse()
    # print(tree)

    # check for errors
    semantic_analyzer = SemanticAnalyzer(tree)
    semantic_analyzer.analyze()

    # interpret language
    interpreter = Interpreter(tree)
    value = interpreter.interpret()
    print(value)
except SyntaxError as ex:
    print(ex.msg)
