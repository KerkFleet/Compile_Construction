"""
Program: Main test for scanner
Programmer: Shelby Kerkvliet
Date: 1/30/2022

Usage: python3 main.py <filename>
"""

import logging
from rdp import Parser
import sys

#check python version
if sys.version_info[0] < 3:
    print("Python3, or a more recent version, is required to run this script")
    exit()

# setup logger
logging.basicConfig(filename='compiler_debug.log', level=logging.DEBUG)


# Get filename from command line
filename=""
if len(sys.argv) > 1:
    filename = str(sys.argv[1])
else:
    print("Usage: python3 main.py <filepath>")
    exit()


# While loop to retrieve tokens until end of file
myparser = Parser(filename)

myparser.Prog()
print("Successfully compiled with no errors.")