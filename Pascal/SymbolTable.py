from Constants import INTEGER
from Constants import REAL
from DataClasses import Symbol, AbstractSymbol


class SymbolTable:
    def __init__(self, enclosed_parent=None):
        self._symbols = {}
        self.enclosed_parent: SymbolTable = enclosed_parent

    def defineBuiltinTypeSymbols(self):
        self.define(Symbol(INTEGER))
        self.define(Symbol(REAL))

    def define(self, symbol: AbstractSymbol):
        self._symbols[symbol.name] = symbol

    def assign(self, var: str, value: Symbol):
        self._symbols[var] = value

    def is_defined(self, var):
        return self.lookup(var) is not None

    def is_valid_type(self, symbol_type):
        return self.is_defined(symbol_type)

    def lookup(self, var) -> Symbol | None:
        cur_var = self._symbols.get(var, None)
        if cur_var is not None:
            return cur_var

        if self.enclosed_parent:
            return self.enclosed_parent.lookup(var)

        return None

    def __str__(self):
        res = ""
        for symbol in self._symbols.values():
            res += str(symbol) + ","
        return f"SymbolTable({res})"
