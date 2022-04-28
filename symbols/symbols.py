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
    cint = 11
    coutt = 12
    endlt = 13
    addopt = 14
    mulopt = 15
    assignopt = 16
    relopt = 17
    lparent = 18
    rparent = 19
    lcurlyt = 20
    rcurlyt = 21
    lbrackett = 22
    rbrackett = 23
    commat = 24
    semicolont = 25
    periodt = 26
    literalt = 27
    numt = 28
    idt = 29
    signopt = 30
    inarrowt = 31
    outarrowt = 32
    eoft = 33
    UNKNOWN = 34
