import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from symbol_table import SymbolTable


def print_symbol_table(manager):
    for i, scope in enumerate(manager.scopes):
        print(f"\n💡 Scope {i}:")
        if not scope:
            print("  (empty)")
        for identifier, symbol_info in scope.items():
            print(f"  {identifier}: {symbol_info}")


if __name__ == "__main__":
    table = SymbolTable()

    # 1. Initialize the symbol table -> Located at global
    table.initSymTab()

    # 2. Add 3 symbols in global scope
    table.addSymbol("temperature")
    table.addSymbol("velocity")
    table.addSymbol("temp")

    # 3. Add 'int' type to temperature and velocity
    table.addAttributeToSymbol("temperature", 0, "type", "int")
    table.addAttributeToSymbol("velocity", 0, "type", "int")

    # 4. Enter new scope
    new_scope = table.enterScope()
    print(f"\nEntered new scope: {new_scope}")

    # 5. Add velocity and position in new scope
    table.addSymbol("velocity")
    table.addSymbol("position")

    # 6. Add 'float' type to velocity
    table.addAttributeToSymbol("velocity", new_scope,  "type", "float")

    # 7. Add 'int' type to position
    table.addAttributeToSymbol("position", new_scope,  "type", "int")

    print(" \n\nScopes's View")
    print("-------------------------------------------")
    print_symbol_table(table)
    print("-------------------------------------------")


    # 8. Check if 'temperature' is in the symbol table
    print(f"\n < Now located in {table.lastScope} Scope >")
    tempInTable = table.symbolInTable("temperature", -1)
    print(f"\n'temperature' in table: {tempInTable}")

    # 9. Check if 'bang' is in the symbol table
    bangInTable = table.symbolInTable("bang", -1)
    print(f"'bang' in table: {bangInTable}")

    # 10. Retrieve 'position' and print type
    print("\n10. 'position' symbol info:")
    positionInfo = table.getSymbol("position", new_scope)
    print(positionInfo)


    # 11. Lookup 'velocity' (should be local, type float)
    print("\n11. Lookup 'velocity':")
    velLookup = table.lookup("velocity")
    print(velLookup)

    # more test. Get 'temperature' (from exited scope)
    print("\n-Additional Test1: getSymbol & lookUp 'temperature' from exited scope:")
    temperatureInfo = table.getSymbol("temperature", new_scope)
    temperatureLookup = table.lookup("temperature")
    print("get symbol: ",temperatureInfo)
    print("look up temperature: ",temperatureLookup,"\n")

    # 12. Exit scope
    table.exitScope()
    print("\n < Exited to global scope. >")

    # 13a. Add memory location to temperature
    table.addAttributeToSymbol("temperature", 0, "MEMORY", "0x800000")

    # 13b. Add memory location to velocity
    table.addAttributeToSymbol("velocity", 0, "MEMORY", "0x800020")
    
    # 13c. Add array info to temp
    table.addAttributeToSymbol("temp", 0, "TYPE", "array")
    table.addAttributeToSymbol("temp", 0, "DIMENSIONS", 2)
    table.addAttributeToSymbol("temp", 0, "DIM_BOUNDS", [15, 10])
    table.addAttributeToSymbol("temp", 0, "MEMORY", "0x800040")

    print(" \n\nScopes's View")
    print("-------------------------------------------")
    print_symbol_table(table)
    print("-------------------------------------------")

    # 14. Get 'temperature' and print attributes
    print("\n14. 'temperature' info:")
    tempInfo = table.getSymbol("temperature", 0)
    print(tempInfo)

    # 15. Lookup 'velocity' using lookup() (should return global one now)
    print("\n15. Lookup 'velocity' (should be global):")
    velocityLookup = table.lookup("velocity")
    print(velocityLookup)

    # 16. Get 'position' (from exited scope)
    print("\n16. Get 'position' from exited scope:")
    positionInfo = table.getSymbol("position", new_scope)
    positionLookup = table.lookup("position")
    print(positionInfo)
    print(positionLookup)

    # 17. Get 'velocity' in global scope -> int
    print("\n17. 'velocity' in global scope:")
    velocityInfo = table.getSymbol("velocity", 0)
    print("look up velocity :",velocityInfo)

    # 18. Try to get 'bang'
    print("\n18. Try to get 'bang':")
    bangInfo = table.getSymbol("bang", -1)
    if bangInfo is None:
        print("  'bang' not found")
    else:
        print(bangInfo)


    