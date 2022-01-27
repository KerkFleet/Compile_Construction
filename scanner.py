from enum import IntEnum
from itertools import islice

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
    rcurlyt = 16
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

# global vars
token = symbol.unknown 
lexeme = ""
ch = ''
lineno = 0
value = 0
valueR = 0.0
literal = ""
resword = []

class scanner:
    def __init__(self, filename):
        global token
        global lexeme
        global ch
        global lineno
        global value
        global valueR
        global literal
        global resword
        token = symbol.unknown
        self.f = open(filename, "r")
        if not self.f:
            print("ERROR: File does not exist")
            quit()
        self.getNextCh()
        resword.append("if")
        resword.append("else")
        resword.append("while")
        resword.append("float")
        resword.append("int")
        resword.append("char")
        resword.append("break")
        resword.append("continue")
        resword.append("void")

    def getNextToken(self):
        global token
        global lexeme
        global ch
        global lineno
        global value
        global valueR
        global literal
        global resword
        while ch.isspace():
            self.getNextCh()
        if not ch:
            self.f.close()
            token = symbol.eoft
            lexeme = ''
            return
        self.processToken()

    def getNextCh(self):
        global token
        global lexeme
        global ch
        global lineno
        global value
        global valueR
        global literal
        global resword
        ch = self.f.read(1)

    def processToken(self):
        global token
        global lexeme
        global ch
        global lineno
        global value
        global valueR
        global literal
        global resword
        lexeme = ch
        self.getNextCh()
        if lexeme[0].isalpha():
            self.processWordToken()
        elif lexeme[0].isnumeric():
            self.processNumToken()
        elif lexeme[0] == '/':
            if ch == '*':
                self.processComment()
            else:
                self.processMulOp()
        elif lexeme[0] == '+' or lexeme[0] == '-' or lexeme[0] == '|':
            self.processAddOp()
        elif lexeme[0] == '*' or lexeme[0] == '%' or lexeme[0] == '&':
            self.processMulOp()
        elif lexeme[0] == '=' or lexeme[0] == '<' or lexeme[0] == '>':
            if ch == '=':
                self.processDoubleToken()
            else:
                self.processSingleToken()
        elif lexeme[0] == '!':
            self.processDoubleToken()
        else:
            self.processSingleToken()

    def processWordToken(self):
        global token
        global lexeme
        global ch
        global lineno
        global value
        global valueR
        global literal
        global resword
        while ch.isalnum() or ch == '_':
            lexeme = lexeme + ch
            self.getNextCh()
        for sym in islice(symbol, symbol.voidt+1):
            if resword[sym] == lexeme:
                token = sym
                return
        token = symbol.idt

    def processNumToken(self):
        global token
        global lexeme
        global ch
        global lineno
        global value
        global valueR
        global literal
        global resword
        dec = False

        while ch.isnumeric() or ch == '.':
            lexeme = lexeme + ch
            if(ch == '.'):
                dec = True
            self.getNextCh()
        token = symbol.numt
        if(dec):
            valueR = float(lexeme)
        else:
            value = int(lexeme)

    def processComment(self):
        global token
        global lexeme
        global ch
        global lineno
        global value
        global valueR
        global literal
        global resword
        while ch != '/':
            self.getNextCh()
        self.getNextCh()

    def processMulOp(self):
        global token
        global lexeme
        global ch
        global lineno
        global value
        global valueR
        global literal
        global resword
        if ch == '&':
            lexeme = lexeme + ch
            self.getNextCh()
        token = symbol.mulopt

    def processAddOp(self):
        global token
        global lexeme
        global ch
        global lineno
        global value
        global valueR
        global literal
        global resword
        if ch == '|':
            lexeme = lexeme + ch
            self.getNextCh()
        token = symbol.addopt

    def processDoubleToken(self):
        global token
        global lexeme
        global ch
        global lineno
        global value
        global valueR
        global literal
        global resword
        lexeme = lexeme + ch
        self.getNextCh()
        token = symbol.relopt

    def processSingleToken(self):
        global token
        global lexeme
        global ch
        global lineno
        global value
        global valueR
        global literal
        global resword
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
        global token
        global lexeme
        global ch
        global lineno
        global value
        global valueR
        global literal
        global resword
        print(token, "   ", lexeme)


myscanner = scanner("test.c")

while token != symbol.eoft:
    myscanner.getNextToken()
    myscanner.displayToken()
