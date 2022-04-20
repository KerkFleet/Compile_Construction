from symbol_table.symbol_table import Symbol_Table
from symbol_table import entry
from symbols.symbols import symbol


class CodeGenerator:
    def __init__(self, sym_tab : Symbol_Table, filename):
        self.visual = True
        self.sym_tab = sym_tab
        self.temp_num = 1
        self.line = 1
        self.tacFile = open(filename, "w")

    def new_temp(self, depth):
        var = "_T" + str(self.temp_num)
        self.temp_num = self.temp_num + 1
        self.sym_tab.insert(var, symbol.idt, depth)
        if(self.temp_num > 99):
            print("Temporary variable overflow")
            exit()
        return self.sym_tab.lookup(var)
    
    def b_var(self, offset):
        if offset < 0:
            var = "_BP" + str(offset)
        else:
            var = "_BP+" + str(offset)
        return var

    def emit(self, code):
        self.tacFile.writelines(code + "\n")
        if self.visual:
            if self.line < 20:
                print(code)
            else:
                input("Press enter to continue...")
                print(code)
                self.line = 1
        self.line = self.line + 1

    def unary_assignment(self, dest, src, operator):
        code = ""
        if not operator:
            code = dest + " = " + src
        else:
            code = dest + " = " + operator + src
        self.emit(code)

    def binary_assignment(self, dest, op1, op2, operator):
        code = dest + " = " + op1 + " " + operator  + " " + op2
        self.emit(code)

    def copy_stat(self, dest, src):
        code = dest + " = " + src
        self.emit(code)
    
    def subroutine_call(self, function):
        code = "call " + function
        self.emit(code)

    def param_stat(self, param):
        code = "push " + param
        self.emit(code)

    def proc_header_stat(self, header):
        code = "proc " + header
        self.emit(code)

    def proc_footer_stat(self, footer):
        code = "endp " + footer + "\n"
        self.emit(code)
