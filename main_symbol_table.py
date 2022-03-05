"""
Program: Main test for symbol table functionality
Programmer: Shelby Kerkvliet
Date: 3/5/2022

Usage: python3 main_symbol_table.py 
"""

from symbol_table.symbol_table import Symbol_Table
from symbols.symbols import symbol

table = Symbol_Table(211)

print("Inserting at depths 1, 2, and 3")
# insert and write at depth 1
table.insert(lexeme="Lexeme test", token=symbol.literalt, depth=1)
table.insert(lexeme=15, token=symbol.integert, depth=1)
table.insert(lexeme=14.3, token=symbol.floatt, depth=1)
table.writeTable(1) 

# insert and write at depth 2
table.insert(lexeme="new string", token=symbol.literalt, depth=2)
table.writeTable(2)

# insert and write at depth 3
table.insert(lexeme=12, token=symbol.integert, depth=3)
table.insert(lexeme=27.556, token=symbol.floatt, depth=3)
table.writeTable(3)

print("\nDeleting depth 3. . .")
table.deleteDepth(3)
table.writeTable(1)
table.writeTable(2)
table.writeTable(3)

print("Looking up lexema 'Lexeme test'...\n")
ptr = table.lookup("Lexeme test")
print("    Lexeme: ", ptr.lexeme)
print("    Token: ", ptr.token)
print("    Depth: ", ptr.depth)


print("\nQuick hash test (technically a private function): ")
print("Hashing lexeme 'testing' twice")
print("Value: ", table._hash('testing'))
print("Value: ", table._hash('testing'))
print("Hashing lexeme '15' and '12.23")
print("Value: ", table._hash(15))
print("Value: ", table._hash(12.23))
