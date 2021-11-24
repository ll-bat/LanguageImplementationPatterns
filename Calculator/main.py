from Parser import Parser
from Interpreter import Interpreter

try:
    parser = Parser("2 - - + 2")
    tree = parser.parse()
    interpreter = Interpreter(tree)
    value = interpreter.interpret()
    print(value)
except SyntaxError as ex:
    print(ex.msg)
