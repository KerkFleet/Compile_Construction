proc main
[BP-2] = 10
[BP-4] = 5
[BP-8] = [BP-2] + [BP-4]
[BP-6] = [BP-8]
[BP-10] = [BP-2] * [BP-4]
[BP-6] = [BP-10]
wrs _S1
wri [BP-4]
wrs _S2
wri [BP-6]
wrs _S3
rdi [BP-2]
rdi [BP-4]
rdi [BP-6]
wrs _S4
wri [BP-2]
[BP-12] = [BP-2] + 10
[BP-6] = [BP-12]
call main
[BP-6] = ax
ax = 0
endp main

