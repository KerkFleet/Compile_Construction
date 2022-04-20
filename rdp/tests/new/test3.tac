proc func
_BP-2 = x / y
_BP-4 = _BP+6 - _BP+4
_BP-6 = _BP-2 + _BP-4
_BP+4 = _BP-6
push _BP+6
push _BP+4
call func
_BP+4 = _AX
endp func

proc main
_BP-2 = b * d
_BP-4 = a + _BP-2
c = _BP-4
push 5
push c
call func
y = _AX
endp main

