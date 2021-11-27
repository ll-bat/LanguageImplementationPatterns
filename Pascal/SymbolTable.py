from Constants import INTEGER
from Constants import REAL
from data_classes import Symbol


class SymbolTable:
    def __init__(self):
        self._symbols = {}

    def defineBuiltinTypeSymbols(self):
        self.define(Symbol(INTEGER))
        self.define(Symbol(REAL))

    def define(self, symbol: Symbol):
        self._symbols[symbol.name] = symbol

    def assign(self, var: str, value: Symbol):
        self._symbols[var] = value

    def is_defined(self, var):
        return self.lookup(var) is not None

    def is_valid_type(self, symbol_type):
        return self.is_defined(symbol_type)

    def lookup(self, var) -> Symbol:
        var = self._symbols.get(var, None)
        return var

    def __str__(self):
        res = ""
        for symbol in self._symbols.values():
            res += str(symbol) + ","
        return f"SymbolTable({res})"
