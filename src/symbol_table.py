# Nahyun Kim
# nahyun.kim.4@stonybrook.edu

import sys

class SymbolInfo:
    def __init__(self, identifier):
        self.identifier = identifier
        self.attributes = dict()  # {'type': 'int', 'memory': 0x800000}

    def add_attribute(self, attr_name, value):
        self.attributes[attr_name] = value

    def get_attribute(self, attr_name):
        return self.attributes.get(attr_name, None)

    def __str__(self):
        return f"{self.identifier} -> {self.attributes}"
    
    def __repr__(self):
        return self.__str__()

class SymbolTable:
    def __init__(self):
        self.initSymTab()

    def initSymTab(self):
        self.scopes = [dict()]  # Only Global Scope exists
        self.currScope = 0
        self.scopeStack = [0]
        self.lastScope = 0

    def enterScope(self):
        self.lastScope += 1
        self.scopes.append(dict())
        self.scopeStack.append(self.lastScope)
        return self.lastScope

    def exitScope(self):
        print("Before exit -> lastScope=", self.lastScope, "scopeStack=", self.scopeStack)
        if len(self.scopeStack) == 0:
            print("Already at global scope.")
        else:
            while len(self.scopeStack) > 1:
                self.scopeStack.pop()
        print("After exit -> lastScope=", self.lastScope, "scopeStack=", self.scopeStack)

    def addSymbol(self, identifier):
        currentScopeIndex = self.scopeStack[-1]
        table = self.scopes[currentScopeIndex]
        if identifier in table:
            return False
        table[identifier] = SymbolInfo(identifier)
        return True

    def addAttributeToSymbol(self, identifier, scope, attr, value):
        if scope >= len(self.scopes):
            return False
        table = self.scopes[scope]
        if identifier not in table:
            return False
        table[identifier].add_attribute(attr, value)
        return True

    def symbolInTable(self, identifier, scope):
        if scope < 0:
            for scope_dict in self.scopes:
                if identifier in scope_dict:
                    return True
            return False
        elif scope < len(self.scopes):
            return identifier in self.scopes[scope]
        else:
            return False

    def getSymbol(self, identifier, scope):
        if scope > len(self.scopes) - 1:
            return None
        else:
            return self.scopes[scope].get(identifier, None)

    def lookup(self, identifier):
        for scopeIndex in reversed(self.scopeStack):
            symbol = self.scopes[scopeIndex].get(identifier, None)
            if symbol:
                return symbol
        return None

# === Phase 4 helper functions ===
symbol_table_instance = SymbolTable()

def insert_symbol(name, type_):
    added = symbol_table_instance.addSymbol(name)
    if added:
        scope = symbol_table_instance.scopeStack[-1]
        symbol_table_instance.addAttributeToSymbol(name, scope, 'type', type_)
    return added

def lookup_symbol_table(name):
    symbol = symbol_table_instance.lookup(name)
    if symbol is None:
        print(f"** Symnbol Table Error: Undeclared variable '{name}'")
        sys.exit(1)  
    return symbol.get_attribute('type')