from enum import Enum


class ErrorCode(Enum):
    UNEXPECTED_TOKEN = "Unexpected token"
    ID_NOT_FOUND = "Identifier not found"
    DUPLICATE_ID = "Duplicate id found"
    LEXER_ERROR = "Lexer error"
    PARSER_ERROR = "Parser error"


class Error(Exception):
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = f'{self.__class__.__name__}: {message}'

    def __str__(self):
        return self.message


class LexerError(Error):
    pass


class ParserError(Error):
    pass


class SemanticError(Error):
    pass
