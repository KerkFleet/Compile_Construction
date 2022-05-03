proc func
wrs _S1
rdi a
b = 10
[BP-4] = 20
[BP-6] = a * b
[BP-8] = [BP-4] + [BP-6]
[BP-2] = [BP-8]
wrs _S2
wri [BP-2]
wrln
ax = 0
endp func

proc main
call func
a = ax
ax = 0
endp main

