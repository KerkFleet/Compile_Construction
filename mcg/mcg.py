

from symbol_table import entry
from symbol_table.symbol_table import Symbol_Table


class MachineCodeGenerator:
    def __init__(self, tacFilename, sym_tab : Symbol_Table):
        self.sym_tab = sym_tab
        self.tacFile = open(tacFilename, "r")
        filename = tacFilename.replace(".tac", ".asm")
        self.asmFile = open(filename, "w")
        self.line =""
        self.asmFile.writelines("     .model small\n")
        self.asmFile.writelines("     .stack 100h\n")
        self.asmFile.writelines("     .data\n")
        self.write_symbol_table()
        self.asmFile.writelines("     .code\n")
        self.asmFile.writelines("     include io.asm\n\n")
                    
    def write_symbol_table(self):
        for i in self.sym_tab.table:
            if i:
                ptr = i
                while ptr:
                    if ptr.entry_type == entry.Entry_Type.stringEntry:
                        self.asmFile.writelines(ptr.lexeme + "  DB  \"" + ptr.entry_details.value + "\",\"$\"\n")
                    elif ptr.entry_type == entry.Entry_Type.varEntry:
                        self.asmFile.writelines(ptr.lexeme + "  DW  ?\n")
                    ptr = ptr.next


    def generate(self):
        self.getNextLine()
        while self.line:
            if "proc" in self.line:
                self.write_proc_header()
            elif "call" in self.line:
                self.write_function_call()
            elif "push" in self.line:
                self.write_push()
            elif " + " in self.line:
                self.write_add()
            elif "wrs" in self.line:
                self.write_string()
            elif "wri" in self.line:
                self.write_int()
            elif "wrln" in self.line:
                self.write_line()
            elif "rdi" in self.line:
                self.read_int()
            elif "*" in self.line:
                self.write_multiply()
            elif "/" in self.line:
                self.write_divide()
            elif "=" in self.line:
                self.write_cpy()
            elif "endp" in self.line:
                self.write_function_footer()
            self.getNextLine()
        self.write_start_proc()

    def write_proc_header(self):
        tokens = self.line.split()
        proc_name = tokens[1]
        entryPtr = self.sym_tab.lookup(proc_name)
        self.asmFile.writelines(proc_name + "   PROC\n")
        self.asmFile.writelines("       push bp\n")
        self.asmFile.writelines("       mov bp,sp\n")
        self.asmFile.writelines("       sub sp," + str(entryPtr.entry_details.size_of_local) + "\n\n")

    def write_push(self):
        tokens = self.line.split()
        self.asmFile.writelines("       mov ax," + tokens[1] + "\n")
        self.asmFile.writelines("       push ax\n\n")
        
    
    def write_string(self):
        tokens = self.line.split()
        self.asmFile.writelines("       mov dx, offset " + tokens[1] + "\n")
        self.asmFile.writelines("       call writestr\n\n")

    def write_int(self):
        tokens = self.line.split()
        self.asmFile.writelines("       mov ax," + tokens[1] + "\n")
        self.asmFile.writelines("       call writeint\n\n")

    def write_line(self):
        self.asmFile.writelines("       call writeln\n\n")

    def read_int(self):
        tokens = self.line.split()
        self.asmFile.writelines("       call readint\n")
        self.asmFile.writelines("       mov " + tokens[1] + ", bx\n\n")

    def write_function_call(self):
        tokens = self.line.split()
        proc_name = tokens[1]
        entryPtr = self.sym_tab.lookup(proc_name)
        self.asmFile.writelines("       call " + proc_name + "\n")
        self.getNextLine()
        tokens = self.line.split()
        self.asmFile.writelines("       mov " + tokens[0] + ", ax\n\n")

    def write_divide(self):
        tokens = self.line.split()
        self.asmFile.writelines("       mov ax," + tokens[2] + "\n")
        self.asmFile.writelines("       cwd" + "\n")
        self.asmFile.writelines("       mov bx," + tokens[4] + "\n")
        self.asmFile.writelines("       cwd" + "\n")
        self.asmFile.writelines("       idiv bx\n")
        self.asmFile.writelines("       mov " + tokens[0] + ",ax\n\n")

    def write_multiply(self):
        tokens = self.line.split()
        self.asmFile.writelines("       mov ax," + tokens[2] + "\n")
        self.asmFile.writelines("       mov bx," + tokens[4] + "\n")
        self.asmFile.writelines("       imul bx\n")
        self.asmFile.writelines("       mov " + tokens[0] + ",ax\n\n")

    def write_add(self):
        tokens = self.line.split()
        self.asmFile.writelines("       mov ax," + tokens[2] + "\n")
        self.asmFile.writelines("       add ax," + tokens[4] + "\n")
        self.asmFile.writelines("       mov " + tokens[0] + ",ax\n\n")

    def write_cpy(self):
        tokens = self.line.split()
        if tokens[0] == "ax":
            self.asmFile.writelines("       mov ax," + tokens[2] + "\n")
        else:
            self.asmFile.writelines("       mov ax," + tokens[2] + "\n")
            self.asmFile.writelines("       mov " + tokens[0] + ",ax\n\n")

    def write_function_footer(self):
        tokens = self.line.split()
        proc_name = tokens[1]
        entryPtr = self.sym_tab.lookup(proc_name)
        self.asmFile.writelines("       add sp," + str(entryPtr.entry_details.size_of_local) + "\n")
        self.asmFile.writelines("       pop bp\n")
        num_params = entryPtr.entry_details.num_of_params
        size_params=0
        if num_params:
            size_params = 2 * num_params
        self.asmFile.writelines("       ret " + str(size_params) + "\n")
        self.asmFile.writelines(proc_name + "   ENDP\n\n")

    def write_start_proc(self):
        self.asmFile.writelines("_startproc    PROC\n")
        self.asmFile.writelines("              mov ax, @data\n")
        self.asmFile.writelines("              mov ds, ax\n")
        self.asmFile.writelines("              call main\n")
        self.asmFile.writelines("              mov ax, 4c00h\n")
        self.asmFile.writelines("              int 21h\n")
        self.asmFile.writelines("_startproc    ENDP\n")
        self.asmFile.writelines("              END _startproc\n\n")

    def getNextLine(self):
        self.line = self.tacFile.readline()
        
    def getNextToken(self):
        while self.ch.isspace():
            if(self.ch == '\n'):
                self.lineNum = self.lineNum + 1
            self.getNextCh()
