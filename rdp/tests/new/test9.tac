proc test1
_BP-2 = 5
_BP-4 = 10
_BP-6 = _BP-2 + _BP-4
c = _BP-6
_BP-8 = _BP-2 + _BP-4
_BP-10 = _BP-8 + c
_AX = _BP-10
endp test1

proc main
call test1
_BP-2 = _AX
_AX = 0
endp main

