from Constants import EOF
from Lexer import Lexer
from Parser import Parser

# lexer = Lexer("1 + 2 * 3 / (1 + 2)")
#
# while lexer.get_current_token().type is not EOF:
#     a = lexer.get_current_token()
#     print(a)
#     lexer.get_next_token()

try:
    parser = Parser("1 + 2 * 3 / (1 + 2) ")
    tree = parser.parse()
    print(tree)
except SyntaxError as ex:
    pass
