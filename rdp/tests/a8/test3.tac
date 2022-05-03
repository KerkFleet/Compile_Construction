proc fun
[BP-4] = [BP+4] * [BP+6]
[BP-6] = [BP-4] + [BP+8]
[BP-2] = [BP-6]
wrs _S1
wri [BP-2]
wrln
ax = 0
endp fun

proc main
a = 5
b = 10
d = 20
push a
push d
push b
call fun
a = ax
ax = 0
endp main

