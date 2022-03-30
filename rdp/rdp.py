'''A class with functionality to parse a 
subset of the C language

    Usage:
    Instantiate with myparser = Parser({filename to parse})
    A simple call to our start variable begins the RDP:
    value = myparser.Prog()

    value will hold the final token, which we can ensure
    is the eoft, necessary for program completion
'''
from symbols.symbols import symbol
from scanner.scanner import scanner
import logging
from symbol_table.symbol_table import Symbol_Table
from symbol_table import entry

class Offset_Node:
    def __init__(self):
        self.offset = 0
        self.next = None

class Parser:
    def __init__(self, filename):
        """
        Initialize scanner to get tokens for parsing
        """
        self.myscanner = scanner(filename)
        self.sym_tab = Symbol_Table(211)
        self.myscanner.getNextToken()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.depth = 0
        self.depth_offset = Offset_Node()
        

    def match(self, desiredToken):
        """
        Function to match desired token to actual token
        """
        if self.myscanner.token == desiredToken:
            # self.logger.debug(f"LINE {self.myscanner.lineNum}: Matched {desiredToken.name} to {self.myscanner.token.name}")
            self.myscanner.getNextToken()
        else:
            self.handleError(desiredToken.name)

    def Prog(self):
        """
        Grammar rule: PROG -> TYPE idt REST PROG | const  idt  =  num ; PROG | e
        Inherits: none
        Synthesizes: none
        """
        if self.myscanner.token == symbol.integert or self.myscanner.token == symbol.floatt or self.myscanner.token == symbol.chart:
            type = self.Type()
            self.check_for_duplicates(self.myscanner.lexeme)
            self.sym_tab.insert(self.myscanner.lexeme, self.myscanner.token, self.depth)
            entryPtr = self.sym_tab.lookup(self.myscanner.lexeme)
            self.match(symbol.idt)
            self.Rest(entryPtr, type)
            self.Prog()
        elif self.myscanner.token == symbol.constt:
            self.match(symbol.constt)
            self.check_for_duplicates(self.myscanner.lexeme)
            self.sym_tab.insert(self.myscanner.lexeme, self.myscanner.token, self.depth)
            entryPtr = self.sym_tab.lookup(self.myscanner.lexeme)
            entryPtr.entry_type = entry.Entry_Type.constEntry
            const_entry = entry.Constant_Entry()
            self.match(symbol.idt)
            self.match(symbol.assignopt)
            if isinstance(self.myscanner.value, int):
                const_entry.var_type = entry.Var_Type.intType
                const_entry.offset = self.depth_offset.offset
                self.depth_offset.offset = self.depth_offset.offset + self.calc_size(entry.Var_Type.intType)
            elif isinstance(self.myscanner.value, float):
                const_entry.var_type = entry.Var_Type.floatType
                const_entry.offset = self.depth_offset.offset
                self.depth_offset.offset = self.depth_offset.offset + self.calc_size(entry.Var_Type.intType)
            const_entry.value = self.myscanner.value
            entryPtr.entry_details = const_entry
            self.match(symbol.numt)
            self.match(symbol.semicolont)
            self.Prog()

    
    def Type(self):
        """
        Grammar rule: TYPE -> int | float | char
        Inherits: none
        Synthesizes: tsyn -> entry.Var_Type.<type> (enum specifying type)
        """
        if self.myscanner.token == symbol.integert:
            self.match(symbol.integert)
            return entry.Var_Type.intType
        elif self.myscanner.token == symbol.floatt:
            self.match(symbol.floatt)
            return entry.Var_Type.floatType
        elif self.myscanner.token == symbol.chart:
            self.match(symbol.chart)
            return entry.Var_Type.charType
        else:
            self.handleError([symbol.integert.name, symbol.floatt.name, symbol.chart.name])
    

    def Rest(self, entryPtr : entry.Entry, type : entry.Var_Type):
        """
        Grammar rule: REST -> (PARAMLIST) COMPOUND | IDTAIL ; PROG
        Inherits: type -> entry.Var_Type.<type> (enum specifying type)
                  entryPtr -> entry.Entry()
        Synthesizes: rsyn -> entry.Function_Entry(),
                            or entry.Constant_Entry(),
                            or entry.Variable_Entry(),
                            (entry_details for an entry.Entry() node)
        """
        if self.myscanner.token == symbol.lparent:
            self.depth_offset.offset = self.depth_offset.offset + self.calc_size(type)
            func_entry = entry.Function_Entry() # initialize what REST will synthesize
            entryPtr.entry_details = func_entry
            entryPtr.entry_type = entry.Entry_Type.functionEntry
            func_entry.return_type = type # get return type
            self.match(symbol.lparent)
            self.depth = self.depth + 1 # update depth
            new_depth_offset = Offset_Node()
            new_depth_offset.next = self.depth_offset
            self.depth_offset = new_depth_offset
            self.ParamList(func_entry) # get param list

            self.match(symbol.rparent)
            self.Compound(func_entry) # get size of locals
        else:
            #build variable entry
            var_entry = entry.Variable_Entry()
            var_entry.var_type = type # get variable type
            var_entry.size = self.calc_size(type) # get variable size
            var_entry.offset = self.depth_offset.offset
            self.depth_offset.offset = self.depth_offset.offset + var_entry.size
            entryPtr.entry_details = var_entry
            entryPtr.entry_type = entry.Entry_Type.varEntry
            self.IdTail(type)
            self.match(symbol.semicolont)
            self.Prog()

    def ParamList(self, func_entry):
        """
        Grammar rule: PARAMLIST -> TYPE idt PARAMTAIL | e
        Inherits: func_entry
        Synthesizes: none
        """
        if self.myscanner.token == symbol.integert or self.myscanner.token == symbol.floatt or self.myscanner.token == symbol.chart:
            type = self.Type()
            # add param node to parameter list
            param = entry.Param_Node()
            param.param_type = type
            param.next = func_entry.param_list
            func_entry.param_list = param

            # add parameter to symbol table
            self.check_for_duplicates(self.myscanner.lexeme)
            self.sym_tab.insert(self.myscanner.lexeme, self.myscanner.token, self.depth)
            entryPtr = self.sym_tab.lookup(self.myscanner.lexeme)

            # create variable entry for parameter entry
            var_entry = entry.Variable_Entry()
            var_entry.var_type = type
            var_entry.size = self.calc_size(type)
            var_entry.offset = self.depth_offset.offset
            self.depth_offset.offset = self.depth_offset.offset + var_entry.size
            entryPtr.entry_details = var_entry
            entryPtr.entry_type = entry.Entry_Type.varEntry

            # update size of locals
            func_entry.size_of_local = func_entry.size_of_local + var_entry.size

            func_entry.num_of_params = func_entry.num_of_params + 1 # increment number of parameters in function entry
            self.match(symbol.idt)
            self.ParamTail(func_entry)

    def ParamTail(self, func_entry):
        """
        Grammar rule: PARAMTAIL -> , TYPE idt PARAMTAIL | e
        Inherits: func_entry
        Synthesizes: none
        """
        if self.myscanner.token == symbol.commat:
            param = entry.Param_Node()
            self.match(symbol.commat)
            type = self.Type()

            # add param node to parameter list
            param = entry.Param_Node()
            param.param_type = type
            param.next = func_entry.param_list
            func_entry.param_list = param

            # add parameter to symbol table
            self.check_for_duplicates(self.myscanner.lexeme)
            self.sym_tab.insert(self.myscanner.lexeme, self.myscanner.token, self.depth)
            entryPtr = self.sym_tab.lookup(self.myscanner.lexeme)

            # create variable entry for parameter entry
            var_entry = entry.Variable_Entry()
            var_entry.var_type = type
            var_entry.size = self.calc_size(type)
            var_entry.offset = self.depth_offset.offset
            self.depth_offset.offset = self.depth_offset.offset + var_entry.size
            entryPtr.entry_details = var_entry
            entryPtr.entry_type = entry.Entry_Type.varEntry

            # update size of locals
            func_entry.size_of_local = func_entry.size_of_local + var_entry.size

            func_entry.num_of_params = func_entry.num_of_params + 1 # increment number of parameters in function entry
            self.match(symbol.idt)
            self.ParamTail(func_entry)

    def Compound(self, func_entry):
        """
        Grammar rule: COMPOUND -> { DECL  STAT_LIST RET_STAT }
        Inherits: func_entry
        Synthesizes: none
        """
        if self.myscanner.token == symbol.lcurlyt:
            self.match(symbol.lcurlyt)
            self.Decl(func_entry)
            self.StatList()
            self.RetStat()
            self.match(symbol.rcurlyt)
            self.sym_tab.writeTable(self.depth)
            self.sym_tab.deleteDepth(self.depth)
            self.depth = self.depth - 1
            old_offset = self.depth_offset
            self.depth_offset = self.depth_offset.next
            del(old_offset)

        else:
            self.handleError(symbol.lcurlyt.name)

    def Decl(self, func_entry):
        """
        Grammar rule: DECL -> TYPE IDLIST | const  idt  =  num ; DECL | e
        Inherits: func_entry
        Synthesizes: none
        """
        if self.myscanner.token == symbol.integert or self.myscanner.token == symbol.floatt or self.myscanner.token == symbol.chart:
            type = self.Type()
            self.IdList(type, func_entry)
        elif self.myscanner.token == symbol.constt:
            self.match(symbol.constt)
            self.check_for_duplicates(self.myscanner.lexeme)
            self.sym_tab.insert(self.myscanner.lexeme, self.myscanner.token, self.depth)
            entryPtr = self.sym_tab.lookup(self.myscanner.lexeme)
            entryPtr.entry_type = entry.Entry_Type.constEntry
            const_entry = entry.Constant_Entry()
            self.match(symbol.idt)
            self.match(symbol.assignopt)
            if isinstance(self.myscanner.value, int):
                const_entry.var_type = entry.Var_Type.intType
                func_entry.size_of_local = func_entry.size_of_local + self.calc_size(entry.Var_Type.intType)
                const_entry.offset = self.depth_offset.offset
                self.depth_offset.offset = self.depth_offset.offset + self.calc_size(entry.Var_Type.intType)
            elif isinstance(self.myscanner.value, float):
                const_entry.var_type = entry.Var_Type.floatType
                func_entry.size_of_local = func_entry.size_of_local + self.calc_size(entry.Var_Type.floatType)
                const_entry.offset = self.depth_offset.offset
                self.depth_offset.offset = self.depth_offset.offset + self.calc_size(entry.Var_Type.floatType)
            const_entry.value = self.myscanner.value
            entryPtr.entry_details = const_entry
            self.match(symbol.numt)
            self.match(symbol.semicolont)
            self.Decl(func_entry)

    def IdList(self, type : entry.Var_Type, func_entry : entry.Function_Entry):
        """
        Grammar rule: IDLIST -> idt IDTAIL ; DECL
        Inherits: type ->
                  func_entry ->
        Synthesizes: none
        """
        if self.myscanner.token == symbol.idt:

            # insert identifier into symbol table
            self.check_for_duplicates(self.myscanner.lexeme)
            self.sym_tab.insert(self.myscanner.lexeme, self.myscanner.token, self.depth)
            entryPtr = self.sym_tab.lookup(self.myscanner.lexeme)

            # build variable entry
            var_entry = entry.Variable_Entry()
            var_entry.var_type = type # get variable type
            var_entry.size = self.calc_size(type) # get variable size
            var_entry.offset = self.depth_offset.offset
            self.depth_offset.offset = self.depth_offset.offset + self.calc_size(type)
            entryPtr.entry_details = var_entry
            entryPtr.entry_type = entry.Entry_Type.varEntry

            func_entry.size_of_local = func_entry.size_of_local + var_entry.size # update size of locals

            self.match(symbol.idt)
            self.IdTail(type, func_entry)
            self.match(symbol.semicolont)
            self.Decl(func_entry)
        else:
            self.handleError(symbol.idt.name)

    def IdTail(self, type : entry.Var_Type, func_entry=None):
        """
        Grammar rule: IDTAIL -> , idt IDTAIL | e
        Inherits: type -> entry.Var_Type.<type> (enum specifying type)
        Synthesizes: none
        """
        if self.myscanner.token == symbol.commat:
            self.match(symbol.commat)

            # insert identifier into symbol table
            self.check_for_duplicates(self.myscanner.lexeme)
            self.sym_tab.insert(self.myscanner.lexeme, self.myscanner.token, self.depth)
            entryPtr = self.sym_tab.lookup(self.myscanner.lexeme)

            # build variable entry
            var_entry = entry.Variable_Entry()
            var_entry.var_type = type 
            var_entry.size = self.calc_size(type) 
            var_entry.offset = self.depth_offset.offset
            self.depth_offset.offset = self.depth_offset.offset + self.calc_size(type)
            entryPtr.entry_details = var_entry
            entryPtr.entry_type = entry.Entry_Type.varEntry

            # update function entry's size of locals if in a function
            if func_entry:
                func_entry.size_of_local = func_entry.size_of_local + var_entry.size

            self.match(symbol.idt)
            self.IdTail(type, func_entry)

    '''STAT_LIST -> e'''
    def StatList(self):
        return

    '''RET_STAT -> e'''
    def RetStat(self):
        return

    def calc_size(self, type):
        if type == entry.Var_Type.charType:
            return 1
        if type == entry.Var_Type.intType:
            return 2
        if type == entry.Var_Type.floatType:
            return 4
    
    def check_for_duplicates(self, lex):
        entryPtr = self.sym_tab.lookup(lex)
        if entryPtr and entryPtr.depth == self.depth:
            print("ERROR: ")
            print("     LINE ", self.myscanner.lineNum)
            print("     Duplicate variable: '", lex, "' previously declared.")
            exit()
        else:
            return


    def handleError(self, desired):
        print("ERROR:")
        print("     LINE ", self.myscanner.lineNum)
        print("     Expected token:  ", desired)
        print("     Received token:  ", self.myscanner.token.name)
        # self.logger.debug(f"ERROR: LINE {self.myscanner.lineNum}: Expected: {desired}, Received: {self.myscanner.token.name}")
        exit()
