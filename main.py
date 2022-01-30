"""
Program: Main test for scanner
Programmer: Shelby Kerkvliet
Date: 1/30/2022

Usage: python3 main.py <filename>
"""

from scanner import scanner
from symbols import symbol
import sys

# Get filename from command line
filename=""
if len(sys.argv) > 1:
    filename = str(sys.argv[1])
else:
    print("Usage: python main.py <filepath>")
    exit()

# Instantiate scanner
myscanner = scanner(filename)

# Headers for token data
print("LineNum".ljust(10, ' '), "Token".ljust(20, ' '), "Lexeme".ljust(15, ' '), "Attribute")

# While loop to retrieve tokens until end of file
while myscanner.token != symbol.eoft:
    myscanner.getNextToken()
    myscanner.displayToken()