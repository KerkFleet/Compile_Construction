proc test1
_BP-4 = _BP+6 * _BP+4
_BP-6 = _BP-4 + 30
_BP-2 = _BP-6
_AX = _BP-2
endp test1

proc main
_BP-2 = 10
_BP-4 = 20
push _BP-4
push _BP-2
call test1
_BP-6 = _AX
_AX = 0
endp main

