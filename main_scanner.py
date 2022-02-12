"""
Program: Main test for scanner
Programmer: Shelby Kerkvliet
Date: 1/30/2022

Usage: python3 main.py <filename>
"""

import sys
from symbols.symbols import symbol
from scanner.scanner import scanner

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


myscanner = scanner(filename)
while(myscanner.token is not symbol.eoft):
    myscanner.getNextToken()
    myscanner.displayToken()