'''
Entry node to be created for hash table lists.
Has 3 types of entries - constant, function, and variable.
All inherit from a generice Entry class
'''


from enum import IntEnum


'''Parent entry class'''
class Entry:
    def __init__(self, lexeme, token, depth):
        self.lexeme = lexeme
        self.token = token
        self.depth = depth
        self.entry_type = None
        self.next = None


class Variable_Entry(Entry):
    def __init__(self, lexeme, token, depth):
        super.__init__(lexeme, token, depth)
        self.var_type = None
        self.offset = None
        self.size = None


class Constant_Entry(Entry):
    def __init__(self, lexeme, token, depth):
        super.__init__(lexeme, token, depth)
        self.var_type = None
        self.offset = None
        self.value = None


class Function_Entry(Entry):
    def __init__(self, lexeme, token, depth):
        super.__init__(lexeme, token, depth)
        self.size_of_local = None
        self.num_of_params = None
        self.return_type = None
        self.param_list = None


'''Node to create a single paramenter entry for the function_entry parameter list'''
class Param_Node:
    def __init__(self):
        self.param_type = None
        self.next = None


'''Enumerated variable type'''
class Var_Type(IntEnum):
    charType = 0
    intType = 1
    floatType = 2


'''Enumerated entry type to specify in Entry'''
class Entry_Type(IntEnum):
    constEntry = 0
    varEntry = 1
    functionEntry = 2
