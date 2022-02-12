from enum import IntEnum

"""Enumerator class for the symbols of the C-- language"""

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
    literalt = 22
    numt = 23
    idt = 24
    eoft = 25
    UNKNOWN = 26
