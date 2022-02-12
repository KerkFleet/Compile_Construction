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
logger = logging.getLogger()
if len(sys.argv) > 2:
    if '-v' in sys.argv:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.disable()
    if '-rdp' in sys.argv:
        logger.addFilter(logging.Filter(name='rdp'))
    if '-scanner':
        logger.addFilter(logging.Filter(name='scanner'))
else:
    pass



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