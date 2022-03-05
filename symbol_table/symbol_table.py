'''A class with functionality to create a 
hash table with chaining, and associated interactive functions
to be used by a recursive descent parser during compilation

    Usage:
    Instantiate with my_symbol_table = Symbol_Table({symbol table size})

    Associated functions can then be used to insert, delete, etc.
    as layed out in the functions' documentation within the class

    symbol table size is recommended to be a larger prime number to prevent
    many collisions
'''
from .entry import Entry

class Symbol_Table:

    '''Initializes an empty array of "size"  '''
    def __init__(self, size):
        self.tablesize = size
        self.table = [None] * self.tablesize
        pass

    '''Creates a new entry and stores it in the list at the hashed location'''
    def insert(self, lexeme, token, depth):
        x = self._hash(lexeme)
        new_entry = Entry(lexeme, token, depth)
        new_entry.next = self.table[x]
        self.table[x] = new_entry

    '''Deletes all nodes in the hash table with the specified depth'''
    def deleteDepth(self, depth):
        for i in range(self.tablesize):
            temp = self.table[i]
            while temp and temp.depth == depth:
                temp = temp.next
            self.table[i] = temp

    '''Returns the node object(pointer) with the specified lexeme'''
    def lookup(self, lexeme):
        x = self._hash(lexeme)
        temp = self.table[x]
        while temp and temp.lexeme != lexeme:
            temp = temp.next
        if temp: 
            return temp
        else:
            return None

    '''Displays hash table and all entries'''
    def writeTable(self, depth):
        print("\nVariables at depth ", depth, "\n")
        for i in range(self.tablesize):
            temp = self.table[i]
            while temp:
                if temp.depth == depth:
                    print("    ", temp.lexeme)
                temp = temp.next

    '''
    - Private function to determine hased location based on lexeme
    - '_' is used to denote a private function(though technically still accessible publicly)
    - Hash algorithm takes 
    '''
    def _hash(self, lexeme): 
        x = 0
        var = lexeme
        if not isinstance(var, str):
            var = str(lexeme)
        for i in range(len(var)):
            x = x + (ord(var[i]) << i) # bit shift value by location in string
        x = x % self.tablesize
        return x
