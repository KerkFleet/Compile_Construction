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
    constt = 9
    addopt = 10
    mulopt = 11
    assignopt = 12
    relopt = 13
    lparent = 14
    rparent = 15
    lcurlyt = 16
    rcurlyt = 17
    lbrackett = 18
    rbrackett = 19
    commat = 20
    semicolont = 21 
    periodt = 22
    literalt = 23
    numt = 24
    idt = 25
    eoft = 26
    UNKNOWN = 27
