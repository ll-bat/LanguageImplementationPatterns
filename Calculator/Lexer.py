from Constants import MINUS, MULT, PLUS, DIV, LPARENT, RPARENT, EOF, INTEGER
from data_classes import Token


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pre_run()
        self.pos = 0
        self.current_token = self.get_next_token()
        self.validate()

    def pre_run(self):
        self.text = self.text.replace(" ", "")

    def error(self, message):
        raise SyntaxError(message)

    def validate(self):
        if len(self.text) < 1:
            self.error("emtpy text")

        char_token = self.get_current_token()
        if char_token.type is not INTEGER:
            self.error("first token error")

    def is_pointer_out_of_text(self):
        return self.pos >= len(self.text)

    def get_position(self):
        return self.pos

    def get_current_token(self):
        return self.current_token

    def go_forward(self):
        # this will match next token and save it in current_token variable
        self.get_next_token()

    def get_character(self, pos):
        if pos >= len(self.text):
            return None
        return self.text[pos]

    def get_current_character(self):
        return self.get_character(self.pos)

    @staticmethod
    def is_digit(num):
        if isinstance(num, str):
            return num.isdigit()
        return False

    def is_not_digit(self, s):
        return self.is_digit(s) is False

    def get_char_type(self, p):
        types = {
            "+": PLUS,
            "-": MINUS,
            "*": MULT,
            "/": DIV,
            "(": LPARENT,
            ")": RPARENT
        }

        element_type = types.get(p, None)
        if element_type is None:
            self.error("Unsupported character " + p)

        return element_type

    def advance(self):
        self.pos = self.pos + 1

    def get_next_token(self) -> Token:
        cur_char = self.get_current_character()

        if cur_char is None:
            self.current_token = Token(EOF, EOF)
            return self.current_token

        if self.is_digit(cur_char):
            while True:
                self.advance()
                char = self.get_current_character()
                if self.is_digit(char):
                    cur_char += char
                else:
                    break
            num = int(cur_char)
            self.current_token = Token(INTEGER, num)
        else:
            self.advance()
            self.current_token = Token(self.get_char_type(cur_char), cur_char)

        return self.current_token
