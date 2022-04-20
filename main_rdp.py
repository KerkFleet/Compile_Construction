"""
Program: Main test for rdp
Programmer: Shelby Kerkvliet
Date: 1/30/2022

Usage: python3 main_rdp.py <filename>
"""

import logging

from rdp.rdp import Parser
from symbols.symbols import symbol
import sys

#check python version
if sys.version_info[0] < 3:
    print("Python3, or a more recent version, is required to run this script")
    exit()

# setup logger
if len(sys.argv) > 2:
    if '-v' in sys.argv:
        logging.basicConfig(level=logging.DEBUG)
        if '-rdp' in sys.argv:
            pass
        if '-scanner':
            pass
    else:
        logging.disable()



# Get filename from command line
filename=""
if len(sys.argv) > 1:
    filename = str(sys.argv[1])
else:
    print("Usage: python3 main.py <filepath>")
    exit()


# Instantiate parser
myparser = Parser(filename)

#begin recursive descent parsing
myparser.Prog()
myparser.match(symbol.eoft)
main = myparser.sym_tab.lookup("main")
if not main:
    print("ERROR: No function 'main' found.")
else:
    print("Successfully compiled with no errors")

