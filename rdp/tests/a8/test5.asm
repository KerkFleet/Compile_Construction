     .model small
     .stack 100h
     .data
     .code
     include io.asm

main   PROC
       push bp
       mov bp,sp
       sub sp,8

       mov ax,10
       mov [BP-2],ax

       mov ax,5
       mov [BP-4],ax

       mov ax,[BP-2]
       cwd
       mov bx,[BP-4]
       cwd
       idiv bx
       mov [BP-8],ax

       mov ax,[BP-8]
       mov [BP-6],ax

       mov ax,[BP-6]
       call writeint

       call writeln

       mov ax,0
       add sp,8
       pop bp
       ret 0
main   ENDP

_startproc    PROC
              mov ax, @data
              mov ds, ax
              call main
              mov ax, 4c00h
              int 21h
_startproc    ENDP
              END _startproc

