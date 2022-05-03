proc double
[BP-2] = [BP+4]
[BP-4] = 2 * [BP+4]
[BP-2] = [BP-4]
ax = [BP-2]
endp double

proc main
b = 5
push b
call double
a = ax
wri a
wrln
ax = 0
endp main

