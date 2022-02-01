"""
Program: Main test for scanner
Programmer: Shelby Kerkvliet
Date: 1/30/2022

Usage: python3 main.py <filename>
"""

from scanner import scanner
from symbols import symbol
import sys

#check python version
if sys.version_info[0] < 3:
    print("Python3, or a more recent version, is required to run this script")
    exit()

# Get filename from command line
filename=""
if len(sys.argv) > 1:
    filename = str(sys.argv[1])
else:
    print("Usage: python3 main.py <filepath>")
    exit()

# Instantiate scanner
myscanner = scanner(filename)

# Headers for token data
print("LineNum".ljust(10, ' '), "Token".ljust(20, ' '), "Lexeme".ljust(30, ' '), "Attribute")

# While loop to retrieve tokens until end of file
while myscanner.token != symbol.eoft:
    myscanner.getNextToken()
    myscanner.displayToken()