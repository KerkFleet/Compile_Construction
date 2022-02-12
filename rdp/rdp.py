from symbols.symbols import symbol
from scanner.scanner import scanner
import logging


class Parser:
    def __init__(self, filename):
        self.myscanner = scanner(filename)
        self.myscanner.getNextToken()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def match(self, desiredToken):
        if self.myscanner.token == desiredToken:
            self.logger.debug(f"LINE {self.myscanner.lineNum}: Matched {desiredToken.name} to {self.myscanner.token.name}")
            self.myscanner.getNextToken()
        else:
            self.handleError(desiredToken.name)

    '''PROG -> TYPE idt REST PROG | e'''
    def Prog(self):
        if self.myscanner.token == symbol.integert or self.myscanner.token == symbol.floatt or self.myscanner.token == symbol.chart:
            self.Type()
            self.match(symbol.idt)
            self.Rest()
            self.Prog()
        else:
            return(symbol.eoft)

    '''TYPE -> int | float | char'''
    def Type(self):
        if self.myscanner.token == symbol.integert:
            self.match(symbol.integert)
        elif self.myscanner.token == symbol.floatt:
            self.match(symbol.floatt)
        elif self.myscanner.token == symbol.chart:
            self.match(symbol.chart)
        else:
            self.handleError([symbol.integert.name, symbol.floatt.name, symbol.chart.name])

    '''REST -> (PARAMLIST) COMPOUND | IDTAIL ; PROG'''
    def Rest(self):
        if self.myscanner.token == symbol.lparent:
            self.match(symbol.lparent)
            self.ParamList()
            self.match(symbol.rparent)
            self.Compound()
        else:
            self.IdTail()
            self.match(symbol.semicolont)
            self.Prog()

    '''PARAMLIST -> TYPE idt PARAMTAIL | e'''
    def ParamList(self):
        if self.myscanner.token == symbol.integert or self.myscanner.token == symbol.floatt or self.myscanner.token == symbol.chart:
            self.Type()
            self.match(symbol.idt)
            self.ParamTail()
        else:
            return

    '''PARAMTAIL -> , TYPE idt PARAMTAIL | e'''
    def ParamTail(self):
        if self.myscanner.token == symbol.commat:
            self.match(symbol.commat)
            self.Type()
            self.match(symbol.idt)
            self.ParamTail()
        else:
            return

    '''COMPOUND -> { DECL  STAT_LIST RET_STAT }'''
    def Compound(self):
        if self.myscanner.token == symbol.lcurlyt:
            self.match(symbol.lcurlyt)
            self.Decl()
            self.StatList()
            self.RetStat()
            self.match(symbol.rcurlyt)
        else:
            self.handleError(symbol.lcurlyt.name)

    '''DECL -> TYPE IDLIST | e'''
    def Decl(self):
        if self.myscanner.token == symbol.integert or self.myscanner.token == symbol.floatt or self.myscanner.token == symbol.chart:
            self.Type()
            self.IdList()
        else:
            return

    '''IDLIST -> idt IDTAIL ; DECL'''
    def IdList(self):
        if self.myscanner.token == symbol.idt:
            self.match(symbol.idt)
            self.IdTail()
            self.match(symbol.semicolont)
            self.Decl()
        else:
            self.handleError(symbol.idt.name)

    '''IDTAIL -> , idt IDTAIL | e'''
    def IdTail(self):
        if self.myscanner.token == symbol.commat:
            self.match(symbol.commat)
            self.match(symbol.idt)
            self.IdTail()
        else:
            return

    '''STAT_LIST -> e'''
    def StatList(self):
        return

    '''RET_STAT -> e'''
    def RetStat(self):
        return

    def handleError(self, desired):
        print("ERROR:")
        print("     LINE ", self.myscanner.lineNum)
        print("     Expected token:  ", desired)
        print("     Received token:  ", self.myscanner.token.name)
        self.logger.debug(f"ERROR: LINE {self.myscanner.lineNum}: Expected: {desired}, Received: {self.myscanner.token.name}")
        exit()