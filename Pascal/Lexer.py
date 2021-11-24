from Constants import *
from data_classes import Token


class Lexer:
    def __init__(self, text):
        self.reserved_keywords = {
            BEGIN: Token(BEGIN, BEGIN),
            END: Token(END, END),
        }
        self.text = text
        self.pre_run()
        self.pos = 0
        self.current_token = self.get_next_token()
        self.validate()

    def pre_run(self):
        # self.text = self.text.replace(" ", "")
        pass

    def error(self, message):
        raise SyntaxError(message)

    def validate(self):
        if len(self.text) < 1:
            self.error("emtpy text")

    def is_pointer_out_of_text(self, pos=None):
        if pos is None:
            pos = self.pos

        return pos >= len(self.text)

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

    def get_current_character(self) -> str:
        return self.get_character(self.pos)

    @staticmethod
    def is_digit(num):
        if isinstance(num, str):
            return num.isdigit()
        return False

    def is_not_digit(self, s):
        return self.is_digit(s) is False

    @staticmethod
    def is_operator(p):
        return p in "+-*/()"

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

    def peek(self):
        if self.is_pointer_out_of_text(self.get_position() + 1):
            return None
        return self.get_character(self.get_position() + 1)

    def get_reserved_keyword_token(self, token_type):
        return self.reserved_keywords.get(token_type)

    def _id(self):
        result = ""
        while self.get_current_character() is not None and self.get_current_character().isalnum():
            result += self.get_current_character()
            self.advance()

        if result in self.reserved_keywords:
            return self.get_reserved_keyword_token(result)

        return Token(ID, result)

    def get_next_token(self) -> Token:
        cur_char = self.get_current_character()
        if cur_char is None:
            self.current_token = Token(EOF, EOF)
            return self.current_token
        if self.is_digit(cur_char):
            # NUMBER
            while True:
                self.advance()
                char = self.get_current_character()
                if self.is_digit(char):
                    cur_char += char
                else:
                    break
            num = int(cur_char)
            self.current_token = Token(INTEGER, num)
        elif cur_char.isalpha():
            # ID
            self.current_token = self._id()
            return self.current_token
        elif self.is_operator(cur_char):
            # OPERATOR (+-*/())
            self.advance()
            self.current_token = Token(self.get_char_type(cur_char), cur_char)
        elif cur_char == '.':
            # DOT
            self.advance()
            self.current_token = Token(DOT, DOT)
        elif cur_char == ';':
            # SEMI
            self.advance()
            self.current_token = Token(SEMI, SEMI)
        elif cur_char == ":" and self.peek() == "=":
            # ASSIGNMENT
            self.advance()
            self.advance()
            self.current_token = Token(ASSIGN, ASSIGN)
        else:
            if cur_char.isspace():
                self.advance()
                return self.get_next_token()
        return self.current_token
