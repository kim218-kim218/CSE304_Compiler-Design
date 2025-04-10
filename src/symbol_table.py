# Nahyun Kim
# nahyun.kim.4@stonybrook.edu

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
        # monotonically increasing sequence of integers
        self.lastScope += 1
        self.scopes.append(dict())
        self.scopeStack.append(self.lastScope)
        return self.lastScope

    def exitScope(self):
        print("Before exit -> lastScope=",self.lastScope ,"scopeStack=", self.scopeStack)
        if len(self.scopeStack)==0:
            print("Already at global scope.")
        else:
            while len(self.scopeStack) >1:
                self.scopeStack.pop()
        
        print("After exit -> lastScope=",self.lastScope ,"scopeStack=", self.scopeStack)


    def addSymbol(self, identifier):
        currentScopeIndex = self.scopeStack[-1]
        table = self.scopes[currentScopeIndex]
        if identifier in table: #already in table -> not needed to add
            return False
        table[identifier] = SymbolInfo(identifier)
        return True

    def addAttributeToSymbol(self, identifier, scope, attr, value):
        if scope >= len(self.scopes):
            return False
        table = self.scopes[scope]

        # if there is no id in this scope, cannot add attribute.
        if identifier not in table:
            return False
        
        table[identifier].add_attribute(attr, value)
        return True

    def symbolInTable(self, identifier, scope):
        # Invalid scope (if negative): Find symbols in all scopes
        if scope < 0:
            for scope_dict in self.scopes:
                if identifier in scope_dict:
                    return True
            return False

        # find the symbol only in that scope
        elif scope < len(self.scopes):
            return identifier in self.scopes[scope]
        else:
            return False

    def getSymbol(self, identifier, scope):
        if scope > len(self.scopes)-1:
            return None
        else:
            return self.scopes[scope].get(identifier, None)

    def lookup(self, identifier):
        for scopeIndex in reversed(self.scopeStack):
            symbol = self.scopes[scopeIndex].get(identifier, None)
            if symbol:
                return symbol
        return None

