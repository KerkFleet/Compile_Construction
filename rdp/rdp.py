'''A class with functionality to parse a 
subset of the C language

    Usage:
    Instantiate with myparser = Parser({filename to parse})
    A simple call to our start variable begins the RDP:
    value = myparser.Prog()

    value will hold the final token, which we can ensure
    is the eoft, necessary for program completion
'''
from rdp.icg.icg import CodeGenerator
from symbols.symbols import symbol
from scanner.scanner import scanner
import logging
from symbol_table.symbol_table import Symbol_Table
from symbol_table import entry

class Offset_Node:
    def __init__(self, start=0):
        self.offset = start
        self.next = None

class Parser:
    def __init__(self, filename):
        """
        Initialize scanner to get tokens for parsing
        """
        self.myscanner = scanner(filename)
        self.sym_tab = Symbol_Table(211)
        filename = filename.replace(".c", ".tac")
        self.icg = CodeGenerator(self.sym_tab, filename)
        self.myscanner.getNextToken()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.depth_offset = Offset_Node()
        self.param_offset = Offset_Node(start=4)
        self.depth = 0
        

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
            self.match(symbol.idt)
            self.match(symbol.assignopt)
            self.build_const_entry(entryPtr)
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
        Synthesizes: none
        """
        if self.myscanner.token == symbol.lparent:
            self.depth_offset.offset = self.depth_offset.offset + self.calc_size(type)
            func_entry = entry.Function_Entry() # initialize what REST will synthesize
            entryPtr.entry_details = func_entry
            entryPtr.entry_type = entry.Entry_Type.functionEntry
            func_entry.return_type = type # get return type
            self.icg.proc_header_stat(entryPtr.lexeme)
            self.match(symbol.lparent)
            self.depth = self.depth + 1 
            new_depth_offset = Offset_Node()
            new_depth_offset.next = self.depth_offset
            self.depth_offset = new_depth_offset
            self.ParamList(func_entry)

            self.match(symbol.rparent)
            self.Compound(func_entry) 
            self.icg.proc_footer_stat(entryPtr.lexeme)
        else:
            self.build_var_entry(entryPtr, type)
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
            # reset offset
            self.param_offset.offset = 4
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
            self.build_var_entry(entryPtr, type, parameter=True)

            # update size of locals
            func_entry.size_of_local = func_entry.size_of_local + self.calc_size(type)

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
            self.build_var_entry(entryPtr, type, parameter=True)

            # update size of locals
            func_entry.size_of_local = func_entry.size_of_local + self.calc_size(type)

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
            self.match(symbol.idt)
            self.match(symbol.assignopt)
            self.build_const_entry(entryPtr)
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

            self.build_var_entry(entryPtr, type)

            func_entry.size_of_local = func_entry.size_of_local + self.calc_size(type)

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
            self.build_var_entry(entryPtr, type)

            # update function entry's size of locals if in a function
            if func_entry:
                func_entry.size_of_local = func_entry.size_of_local + self.calc_size(type)

            self.match(symbol.idt)
            self.IdTail(type, func_entry)

    def RetStat(self):
        """
        Grammar rule: RET_STAT -> returnt Expr ; 
        Inherits: 
        Synthesizes: none
        """
        self.match(symbol.returnt)
        syn = self.Expr()
        self.icg.copy_stat("_AX", syn)
        self.match(symbol.semicolont)


    def StatList(self):
        """
        Grammar rule: STAT_LIST -> Statement ; StatList | e 
        Inherits: 
        Synthesizes: none
        """
        if self.myscanner.token == symbol.idt:
            self.Statement()
            self.match(symbol.semicolont)
            self.StatList()

    def Statement(self):
        """
        Grammar rule: Statement -> AssignStat | IOStat
        Inherits: 
        Synthesizes: none
        """
        if self.myscanner.token == symbol.idt:
            self.AssignStat()
        else:
            self.IOStat()

    def AssignStat(self):
        """
        Grammar rule: AssignStat -> idt = Expr | idt = FunctionCall
        Inherits: 
        Synthesizes: none
        """
        self.check_declaration(self.myscanner.lexeme)
        entryPtr = self.sym_tab.lookup(self.myscanner.lexeme)
        self.match(symbol.idt)
        self.match(symbol.assignopt)
        syn = None
        if self.myscanner.token == symbol.idt:
            entryPtr2 = self.sym_tab.lookup(self.myscanner.lexeme)
            if entryPtr2.entry_type == entry.Entry_Type.functionEntry:
                syn = self.FunctionCall()
            else:
                syn = self.Expr()
        else:
            syn = self.Expr()
        if entryPtr.depth == 0:
            self.icg.copy_stat(entryPtr.lexeme, syn)
        else:
            reg = self.icg.b_var(entryPtr.entry_details.offset)
            self.icg.copy_stat(reg, syn)


    def IOStat(self):
        """
        Grammar rule: IOStat -> e
        Inherits: 
        Synthesizes: none
        """
        return

    def Expr(self):
        """
        Grammar rule:  Expr -> Realtion
        Inherits: 
        Synthesizes: none
        """
        syn = self.Realtion()
        return syn

    def Realtion(self):
        """
        Grammar rule: Realtion -> SimpleExpr
        Inherits: 
        Synthesizes: none
        """
        syn = self.SimpleExpr()
        return syn

    def SimpleExpr(self):
        """
        Grammar rule: SimpleExpr -> Signop Term MoreTerm
        Inherits: 
        Synthesizes: none
        """
        sign = self.Signop()
        tsyn = self.Term(sign)
        syn = self.MoreTerm(tsyn)
        return syn

    def MoreTerm(self, min):
        """
        Grammar rule: MoreTerm -> Addop Term MoreTerm | e
        Inherits: 
        Synthesizes: none
        """
        syn = min
        if self.myscanner.token == symbol.addopt:
            asyn = self.Addop()
            tsyn = self.Term("")
            syn = self.icg.new_temp(self.depth)
            self.build_var_entry(syn, entry.Var_Type.intType)
            syn = self.icg.b_var(syn.entry_details.offset)
            self.icg.binary_assignment(syn, min, tsyn, asyn)
            syn = self.MoreTerm(syn)
        return syn


    def Term(self, tin):
        """
        Grammar rule: Term -> Factor MoreFactor
        Inherits: 
        Synthesizes: none
        """
        fsyn = self.Factor()
        if tin:
            temp = self.icg.new_temp(self.depth)
            self.build_var_entry(temp, entry.Var_Type.intType)
            temp = self.icg.b_var(temp.entry_details.offset)
            self.icg.unary_assignment(temp, fsyn, tin)
            fsyn = temp
        msyn = self.MoreFactor(fsyn)
        return msyn

    def MoreFactor(self, min):
        """
        Grammar rule: MoreFactor -> Mulop Factor MoreFactor | e
        Inherits: 
        Synthesizes: none
        """
        syn = min
        if self.myscanner.token == symbol.mulopt:
            msyn = self.Mulop()
            fsyn = self.Factor()
            syn = self.icg.new_temp(self.depth)
            self.build_var_entry(syn, entry.Var_Type.intType)
            syn = self.icg.b_var(syn.entry_details.offset)
            self.icg.binary_assignment(syn, min, fsyn, msyn)
            syn = self.MoreFactor(syn)
        return syn


    def Factor(self):
        """
        Grammar rule: Factor -> id | num | (Expr)
        Inherits: 
        Synthesizes: none
        """
        if self.myscanner.token == symbol.idt:
            self.check_declaration(self.myscanner.lexeme)
            syn = self.sym_tab.lookup(self.myscanner.lexeme)
            self.match(symbol.idt)
            if syn.entry_type == entry.Entry_Type.constEntry:
                return str(syn.entry_details.value)
            if syn.depth == 0:
                return syn.lexeme
            else:
                syn = self.icg.b_var(syn.entry_details.offset)
                return syn
        elif self.myscanner.token == symbol.numt:
            syn = self.myscanner.lexeme
            self.match(symbol.numt)
            return syn
        elif self.myscanner.token == symbol.lparent:
            self.match(symbol.lparent)
            syn = self.Expr()
            self.match(symbol.rparent)
            return syn
        else:
            self.handleError([symbol.idt, symbol.numt, symbol.lparent])

    def Addop(self):
        """
        Grammar rule: Addop -> + | - | ||
        Inherits: 
        Synthesizes: none
        """
        syn = self.myscanner.lexeme
        self.match(symbol.addopt)
        return syn

    def Mulop(self):
        """
        Grammar rule: Mulop -> * | / | &&
        Inherits: 
        Synthesizes: none
        """
        syn = self.myscanner.lexeme
        self.match(symbol.mulopt)
        return syn

    def Signop(self):
        """
        Grammar rule: Signop -> ! | - | e
        Inherits: 
        Synthesizes: none
        """
        syn = ""
        if self.myscanner.token == symbol.signopt:
            syn = self.myscanner.lexeme
            self.match(symbol.signopt)
        elif self.myscanner.token == symbol.addopt and self.myscanner.lexeme == '-':
            syn = self.myscanner.lexeme
            self.match(symbol.addopt)
        return syn

    def FunctionCall(self):
        """
        Grammar rule: FunctionCall -> idt ( Params )
        Inherits: 
        Synthesizes: none
        """
        self.check_declaration(self.myscanner.lexeme)
        syn = self.myscanner.lexeme
        self.match(symbol.idt)
        self.match(symbol.lparent)
        self.Params()
        self.icg.subroutine_call(syn)
        self.match(symbol.rparent)
        return "_AX"

    def Params(self):
        """
        Grammar rule: Params -> idt ParamsTail | num ParamsTail | e
        Inherits: none
        Synthesizes: none
        """
        if self.myscanner.token == symbol.idt:
            self.check_declaration(self.myscanner.lexeme)
            syn = self.sym_tab.lookup(self.myscanner.lexeme)
            self.match(symbol.idt)
            self.ParamsTail()
            if syn.depth == 0:
                self.icg.param_stat(syn.lexeme)
            else:
                syn = self.icg.b_var(syn.entry_details.offset)
                self.icg.param_stat(syn)
        elif self.myscanner.token == symbol.numt:
            syn = self.myscanner.lexeme
            self.match(symbol.numt)
            self.ParamsTail()
            self.icg.param_stat(syn)
        else:
            return

    def ParamsTail(self):
        """
        Grammar rule: ParamsTail -> , idt ParamsTail | , num ParamsTail | e
        Inherits: none
        Synthesizes: none
        """
        if self.myscanner.token == symbol.commat:
            self.match(symbol.commat)
            if self.myscanner.token == symbol.idt:
                self.check_declaration(self.myscanner.lexeme)
                syn = self.sym_tab.lookup(self.myscanner.lexeme)
                self.match(symbol.idt)
                self.ParamsTail()
                if syn.depth == 0:
                    self.icg.param_stat(syn.lexeme)
                else:
                    syn = self.icg.b_var(syn.entry_details.offset)
                    self.icg.param_stat(syn)
            else:
                syn = self.myscanner.lexeme
                self.match(symbol.numt)
                self.ParamsTail()
                self.icg.param_stat(syn)


    def calc_size(self, type):
        if type == entry.Var_Type.charType:
            return 1
        if type == entry.Var_Type.intType:
            return 2
        if type == entry.Var_Type.floatType:
            return 4
    
    def build_var_entry(self, entryPtr, type, parameter=False):
        var_entry = entry.Variable_Entry()
        var_entry.var_type = type 
        var_entry.size = self.calc_size(type) 
        if parameter:
            var_entry.offset = self.param_offset.offset
            self.param_offset.offset = self.param_offset.offset + self.calc_size(type)
        else:
            self.depth_offset.offset = self.depth_offset.offset - self.calc_size(type)
            var_entry.offset = self.depth_offset.offset
        entryPtr.entry_details = var_entry
        entryPtr.entry_type = entry.Entry_Type.varEntry
    
    def build_const_entry(self, entryPtr):
        const_entry = entry.Constant_Entry()
        if isinstance(self.myscanner.value, int):
            const_entry.var_type = entry.Var_Type.intType
            self.depth_offset.offset = self.depth_offset.offset - self.calc_size(entry.Var_Type.intType)
            const_entry.offset = self.depth_offset.offset
        elif isinstance(self.myscanner.value, float):
            const_entry.var_type = entry.Var_Type.floatType
            self.depth_offset.offset = self.depth_offset.offset - self.calc_size(entry.Var_Type.floatType)
            const_entry.offset = self.depth_offset.offset
        const_entry.value = self.myscanner.value
        entryPtr.entry_details = const_entry

    def build_func_entry(self):
        pass

    def check_for_duplicates(self, lex):
        entryPtr = self.sym_tab.lookup(lex)
        if entryPtr and entryPtr.depth == self.depth:
            print("ERROR: ")
            print("     LINE ", self.myscanner.lineNum)
            print("     Duplicate variable: '", lex, "' previously declared.")
            exit()
        else:
            return
        
    def check_declaration(self, lex):
        ptr = self.sym_tab.lookup(lex)
        while ptr:
            if ptr.lexeme == lex:
                return
            ptr = ptr.next
        print("ERROR: ")
        print("     LINE ", self.myscanner.lineNum)
        print("     Undeclared variable: '", lex)
        exit()

    def handleError(self, desired):
        print("ERROR:")
        print("     LINE ", self.myscanner.lineNum)
        print("     Expected token:  ", desired)
        print("     Received token:  ", self.myscanner.token.name)
        # self.logger.debug(f"ERROR: LINE {self.myscanner.lineNum}: Expected: {desired}, Received: {self.myscanner.token.name}")
        exit()
