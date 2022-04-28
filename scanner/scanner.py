"""A class with the functionality of the scanner portion of a compiler
   The scanner recognizes tokens from a limited version of the C language

    Usage:
    Instantiate scanner object
    While scanner.token != eoft
        Call scanner.getNextToken
        Optional: call scanner.displayToken
        Use token as needed
    
    Each call to scanner.getNextToken sets the scanner's
    state to hold the current token, lexeme, line number,
    and associated attributes. Current data is wiped on
    each subsequent call to getNextToken

"""

from symbols.symbols import symbol
from itertools import islice
import logging




class scanner:
    '''Initializes scanner with associated global variables, opens file, and prime reads first char'''
    def __init__(self, filename):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.attribute = ''
        self.lineNum = 1
        self.token = symbol.UNKNOWN 
        self.lexeme = ""
        self.ch = ''
        self.value = 0
        self.literal = ""
        self.resword = []
        self.f = open(filename, "r")
        if not self.f:
            print("ERROR: File does not exist")
            quit()
        self.getNextCh()
        self.resword.append("if")
        self.resword.append("else")
        self.resword.append("while")
        self.resword.append("float")
        self.resword.append("int")
        self.resword.append("char")
        self.resword.append("break")
        self.resword.append("continue")
        self.resword.append("void")
        self.resword.append("const")
        self.resword.append("return")
        self.resword.append("cin")
        self.resword.append("cout")
        self.resword.append("endl")

    '''Retrieves next token in file. Returns token in scanner.token '''
    def getNextToken(self):
        while self.ch.isspace():
            if(self.ch == '\n'):
                self.lineNum = self.lineNum + 1
            self.getNextCh()

        if not self.ch:
            self.f.close()
            self.token = symbol.eoft
            self.lexeme = ''
            self.attribute = ''
            return
        self.processToken()
        # self.logger.debug(f"LINE {self.lineNum}: token->{self.token.name}, lexeme->{self.lexeme}, attribute->{self.attribute}")

    '''Function to read next char from file. Returned in scanner.ch'''
    def getNextCh(self):
        self.ch = self.f.read(1)

    '''Processes next token based on current char and one look ahead char. Retrieves attributes for token if any exist'''
    def processToken(self):
        self.lexeme = self.ch
        self.getNextCh()
        if self.lexeme[0].isalpha():
            self.processWordToken()
        elif self.lexeme[0].isnumeric():
            self.processNumToken()
        elif self.lexeme[0] == '/':
            if self.ch == '*':
                self.processComment()
            else:
                self.processMulOp()
        elif self.lexeme[0] == '+' or self.lexeme[0] == '-' or self.lexeme[0] == '|':
            self.processAddOp()
        elif self.lexeme[0] == '*' or self.lexeme[0] == '%' or self.lexeme[0] == '&':
            self.processMulOp()
        elif self.lexeme[0] == '=' or self.lexeme[0] == '<' or self.lexeme[0] == '>':
            if self.ch == '=':
                self.processDoubleToken()
            else:
                self.processSingleToken()
        elif self.lexeme[0] == '!':
            if self.ch == '=':
                self.processDoubleToken()
            else:
                self.processSingleToken()
        else:
            self.processSingleToken()
        self.getAttributes()

    '''Processes a word token and sets self.token'''
    def processWordToken(self):
        counter = 1
        too_large = False
        while self.ch.isalnum() or self.ch == '_':
            self.lexeme = self.lexeme + self.ch
            self.getNextCh()
            counter = counter + 1
            if counter == 28:
                too_large = True
                self.token = symbol.UNKNOWN
                print("Identifier must be 27 characters or less")
        if too_large:
            return
        for sym in islice(symbol, symbol.endlt+1):
            if self.resword[sym] == self.lexeme:
                self.token = sym
                return
        self.token = symbol.idt

    '''Processes num token and sets associated attribute'''
    def processNumToken(self):
        dec = False
        while self.ch.isnumeric():
            self.lexeme = self.lexeme + self.ch
            self.getNextCh()
        if self.ch == '.':
            self.lexeme = self.lexeme + self.ch
            dec = True
            self.getNextCh()
            if not self.ch.isnumeric():
                self.token = symbol.UNKNOWN
                return
        if dec:
            while self.ch.isnumeric():
                self.lexeme = self.lexeme + self.ch
                self.getNextCh()
        self.token = symbol.numt
        if dec:
            self.value = float(self.lexeme)
        else:
            self.value = int(self.lexeme)

    '''Removes comments from file and recursively calls scanner.getNextToken()'''
    def processComment(self):
        self.getNextCh()
        while self.ch:
            self.getNextCh()
            if self.ch == '*':
                self.getNextCh()
                if self.ch == '/':
                    break
            if self.ch == '\n':
                self.lineNum = self.lineNum + 1
        if not self.ch:
            print("ERROR: Opening '/*' has no matching '*/'")
            self.token = symbol.UNKNOWN
            return
        self.getNextCh()
        self.getNextToken()

    '''Processes multiplication operators. Sets error state if incorrect operator'''
    def processMulOp(self):
        if self.lexeme == '&':
            if self.ch == '&':
                self.lexeme = self.lexeme + self.ch
                self.getNextCh()
            else: 
                self.token = symbol.UNKNOWN
                return
        self.token = symbol.mulopt

    '''Processes addition operators. Sets error state if incorrect operator'''
    def processAddOp(self):
        if self.lexeme == '|':
            if self.ch == '|':
                self.lexeme = self.lexeme + self.ch
                self.getNextCh()
            else:
                self.token = symbol.UNKNOWN 
                return
        self.token = symbol.addopt

    '''Processes all doulbe relational operators'''
    def processDoubleToken(self):
        self.lexeme = self.lexeme + self.ch
        self.getNextCh()
        self.token = symbol.relopt

    '''Processes all single char tokens. Sets error state if token is unrecognized.'''
    def processSingleToken(self):
        if self.lexeme == '(':
            self.token = symbol.lparent
        elif self.lexeme == ')':
            self.token = symbol.rparent
        elif self.lexeme == '{':
            self.token = symbol.lcurlyt
        elif self.lexeme == '}':
            self.token = symbol.rcurlyt
        elif self.lexeme == '[':
            self.token = symbol.lbrackett
        elif self.lexeme == ']':
            self.token = symbol.rbrackett
        elif self.lexeme == ',':
            self.token = symbol.commat
        elif self.lexeme == ';':
            self.token = symbol.semicolont
        elif self.lexeme == '.':
            self.token = symbol.periodt
        elif self.lexeme == '"':
            self.token = symbol.literalt
            self.processLiteral()
        elif self.lexeme == '>' and self.ch == '>':
            self.lexeme = self.lexeme + self.ch
            self.getNextCh()
            self.token = symbol.inarrowt
        elif self.lexeme == '<' and self.ch == '<':
            self.lexeme = self.lexeme + self.ch
            self.getNextCh()
            self.token = symbol.outarrowt
        elif self.lexeme == '>' or self.lexeme == '<':
            self.token = symbol.relopt
        elif self.lexeme == '=':
            self.token = symbol.assignopt
        elif self.lexeme == '!':
            self.token = symbol.signopt
        else:
            self.token = symbol.UNKNOWN
    
    '''Processes literal tokens. Stores literal in scanner.literal'''
    def processLiteral(self):
        lit = ""
        while self.ch != '"':
            if self.ch == '\n':
                self.ch = ''
                self.lineNum = self.lineNum + 1
            lit = lit + self.ch
            self.getNextCh()
            if not self.ch:
                print("ERROR: Literal has no closing quotation")
                self.token = symbol.UNKNOWN
                return
        self.literal = lit
        self.lexeme = self.literal[:27]
        self.getNextCh()

    '''Displays current line number, token, lexeme, and associated attributes if they exist'''
    def displayToken(self):
        print(str(self.lineNum).ljust(10, ' '), str(self.token.name).ljust(20, ' '), self.lexeme.ljust(30, ' '), self.attribute)

    '''Determines the current attributes, if any, and stores them in scanner.attribute'''
    def getAttributes(self):
        if self.token == symbol.numt:
            self.attribute = self.value
        elif self.token == symbol.literalt:
            self.attribute = self.literal
        elif self.token == symbol.UNKNOWN:
            self.attribute = "INVALID TOKEN"
        else:
            self.attribute = ''


