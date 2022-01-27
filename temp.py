
from enum import IntEnum
from itertools import islice

# global vars

class symbol(IntEnum):
    ift = 0
    elset = 1
    whilet = 2
    floatt = 3
    integert = 4
    chart = 5
    breakt = 6
    continuet = 7
    voidt = 8
    addopt = 9
    mulopt = 10
    assignopt = 11
    relopt = 12
    lparent = 13
    rparent = 14
    lcurlyt = 15
    rcurlt = 16
    lbrackett = 17
    rbrackett = 18
    commat = 19
    semicolont = 20 
    periodt = 21
    quotationt = 22
    numt = 23
    idt = 24
    eoft = 25
    unknown = 26


class scanner:
    def __init__(self, filename):
        self.token = symbol.unknown 
        self.lexeme = ""
        self.ch = ''
        self.lineno = 0
        self.value = 0
        self.valueR = 0.0
        self.literal = ""
        self.resword = []

        self.token = symbol.unknown
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

    def getNextToken(self):
        while self.ch.isspace():
            self.getNextCh()
            if not self.ch:
                self.f.close()
                self.token = symbol.eoft
                break
        self.processToken()

    def getNextCh(self):
        self.ch = self.f.read(1)

    def processToken(self):
        self.lexeme = self.ch
        self.getNextCh()
        if self.lexeme[0].isalpha:
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
                self.processSingleToken
        elif self.lexeme[0] == '!':
            self.processDoubleToken()
        else:
            self.processSingleToken()

    def processWordToken(self):
        while self.ch.isalnum or self.ch == '_':
            lexeme = lexeme + self.ch
            self.getNextCh()
        for sym in islice(symbol, symbol.voidt+1):
            if self.resword[sym] == lexeme:
                self.token = sym
                return
        self.token = symbol.idt

    def processNumToken(self):
        while self.ch.isnumeric() or self.ch == '.':
            lexeme = lexeme + self.ch
            if(self.ch == 'x'):
                dec = True
        self.token = symbol.numt
        if(dec):
            self.valueR = float(lexeme)
        else:
            self.value = int(lexeme)

    def processComment(self):
        while self.ch != '/':
            self.getNextCh()
        self.getNextCh()

    def processMulOp(self):
        if self.ch == '&':
            self.lexeme = self.lexeme + self.ch
            self.getNextCh()
        token = symbol.mulopt

    def processAddOp(self):
        if self.ch == '|':
            self.lexeme = self.lexeme + self.ch
            self.getNextCh()
        self.token = symbol.addopt

    def processDoubleToken(self):
        self.lexeme = self.lexeme + self.ch
        self.getNextCh()
        self.token = symbol.relopt

    def processSingleToken(self):
        if lexeme == '(':
            token = symbol.lparent
        if lexeme == ')':
            token = symbol.rparent
        if lexeme == '{':
            token = symbol.lcurlyt
        if lexeme == '}':
            token = symbol.rcurlyt
        if lexeme == '[':
            token = symbol.lbrackett
        if lexeme == ']':
            token = symbol.rbrackett
        if lexeme == ',':
            token = symbol.commat
        if lexeme == ';':
            token = symbol.semicolont
        if lexeme == '.':
            token = symbol.periodt
        if lexeme == '"':
            token = symbol.quotationt
        if lexeme == '>' or lexeme == '<':
            token = symbol.relopt
        if lexeme == '=':
            token = symbol.assignopt

    def displayToken(self):
        print(token, "   ", lexeme)


myscanner = scanner("test.c")

while(token != symbol.eoft):
    myscanner.getNextToken()
    myscanner.displayToken()