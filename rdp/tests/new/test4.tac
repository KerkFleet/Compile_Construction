proc main
_BP-2 = b / c
_BP-4 = a + _BP-2
_BP-6 = _BP-4 + d
c = _BP-6
endp main

proc func
_BP-6 = _BP-2 / _BP-4
_BP-8 = _BP+6 - _BP+4
_BP-10 = _BP-6 + _BP-8
_BP+4 = _BP-10
endp func

