from constants import *
from data_classes import Token, Str
from errors import LexerError, ErrorCode
from reserved import RESERVED_KEYWORDS


class Lexer:
    def __init__(self, text):
        self.pos = 0
        self.text = text
        self.lineno = 1
        self.column = 1
        self.current_token = self.get_next_token()

    def error(self, message):
        s = f'Lexer error on {self.get_current_character()};' \
            f' line: {self.lineno};' \
            f' column: {self.column} ' \
            f' message: {message}'

        raise LexerError(ErrorCode, s)

    def is_pointer_out_of_text(self, pos=None):
        if pos is None:
            pos = self.pos

        return pos >= len(self.text)

    def get_position(self):
        return self.pos

    def get_current_token(self):
        return self.current_token

    def peek_next_token(self):
        cur_pos = self.pos
        current_token = self.get_current_token()
        next_token = self.get_next_token()
        self.pos = cur_pos
        self.current_token = current_token
        return next_token

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
            "/": FLOAT_DIV,
            "(": LPARENT,
            ")": RPARENT
        }

        element_type = types.get(p, None)
        if element_type is None:
            self.error("Unsupported character " + p)

        return element_type

    def advance(self):
        if self.get_current_character() == '\n':
            self.lineno += 1
            self.column = 1
        else:
            self.column += 1

        self.pos = self.pos + 1

    def peek(self):
        if self.is_pointer_out_of_text(self.get_position() + 1):
            return None
        return self.get_character(self.get_position() + 1)

    @staticmethod
    def get_reserved_keyword_token(token_type):
        return RESERVED_KEYWORDS.get(token_type)

    def _id(self):
        result = ""
        while self.get_current_character() is not None and self.get_current_character().isalnum():
            result += self.get_current_character()
            self.advance()

        if result in RESERVED_KEYWORDS:
            return self.get_reserved_keyword_token(result)

        return Token(ID, result)

    def _string(self):
        cur_char = self.get_current_character()
        string = ""
        self.advance()
        while self.get_current_character() != cur_char:
            string += self.get_current_character()
            self.advance()
        self.advance()
        return Token(STRING, string)

    def _number(self):
        cur_char = self.get_current_character()
        while True:
            self.advance()
            char = self.get_current_character()
            if self.is_digit(char) or char == '.':
                cur_char += char
            else:
                break

        cnt = cur_char.count('.')
        if cnt > 1:
            self.error('incorrect number ' + cur_char)

        if cnt == 0:
            num = int(cur_char)
            return Token(INTEGER, num)
        else:
            num = float(cur_char)
            return Token(FLOAT, num)

    def skip_comment(self):
        while self.get_current_character() != "}":
            self.advance()
        self.advance()

    def get_next_token(self) -> Token:
        cur_char = self.get_current_character()
        if cur_char is None:
            self.current_token = Token(EOF, EOF)
            return self.current_token
        if self.is_digit(cur_char):
            # NUMBER
            self.current_token = self._number()
            return self.current_token
        elif cur_char in ("'", '"'):
            # STRING
            self.current_token = self._string()
            return self.current_token
        elif cur_char.isalpha():
            # ID
            self.current_token = self._id()
            return self.current_token
        elif self.is_operator(cur_char):
            # OPERATOR (+-*/())
            self.advance()
            self.current_token = Token(self.get_char_type(cur_char), cur_char)
            return self.current_token
        elif cur_char == '.':
            # DOT
            self.advance()
            self.current_token = Token(DOT, DOT)
            return self.current_token
        elif cur_char == ';':
            # SEMI
            self.advance()
            self.current_token = Token(SEMI, SEMI)
            return self.current_token
        elif cur_char == ":" and self.peek() == "=":
            # ASSIGNMENT
            self.advance()
            self.advance()
            self.current_token = Token(ASSIGN, ASSIGN)
            return self.current_token
        elif cur_char == "{":
            self.skip_comment()
            return self.get_next_token()
        elif cur_char == ":":
            self.advance()
            self.current_token = Token(COLON, COLON)
            return self.current_token
        elif cur_char == ',':
            self.advance()
            self.current_token = Token(COMMA, COMMA)
            return self.current_token
        else:
            if cur_char.isspace():
                while self.get_current_character() is not None and self.get_current_character().isspace():
                    self.advance()
                return self.get_next_token()
            self.error('syntax error "' + cur_char + '" is not valid character')
        self.error('unrecognized character ' + cur_char)
