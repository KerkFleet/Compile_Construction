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
    returnt= 10
    addopt = 11
    mulopt = 12
    assignopt = 13
    relopt = 14
    lparent = 15
    rparent = 16
    lcurlyt = 17
    rcurlyt = 18
    lbrackett = 19
    rbrackett = 20
    commat = 21
    semicolont = 22
    periodt = 23
    literalt = 24
    numt = 25
    idt = 26
    signopt = 27
    eoft = 28
    UNKNOWN = 29
