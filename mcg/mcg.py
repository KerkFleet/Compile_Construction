

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
            elif "+" in self.line:
                self.write_add()
            elif "=" in self.line:
                self.write_cpy()
            self.getNextLine()

    def write_proc_header(self):
        proc_name = self.line[5:len(self.line)-1]
        entryPtr = self.sym_tab.lookup(proc_name)
        self.asmFile.writelines(proc_name + "   PROC\n")
        self.asmFile.writelines("       push bp\n")
        self.asmFile.writelines("       mov bp,sp\n")
        self.asmFile.writelines("       sub sp," + str(entryPtr.entry_details.size_of_local) + "\n\n")

    def write_add(self):
        tokens = self.line.split()
        self.asmFile.writelines("       mov ax," + tokens[2] + "\n")
        self.asmFile.writelines("       add ax," + tokens[4] + "\n")
        self.asmFile.writelines("       mov " + tokens[0] + ",ax\n\n")

    def write_cpy(self):
        tokens = self.line.split()
        self.asmFile.writelines("       mov ax," + tokens[2] + "\n")
        self.asmFile.writelines("       mov " + tokens[0] + ",ax\n\n")

    def getNextLine(self):
        self.line = self.tacFile.readline()
        
    def getNextToken(self):
        while self.ch.isspace():
            if(self.ch == '\n'):
                self.lineNum = self.lineNum + 1
            self.getNextCh()
