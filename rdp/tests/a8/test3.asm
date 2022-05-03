     .model small
     .stack 100h
     .data
_S1  DB  "The answer is ","$"
a  DW  ?
b  DW  ?
d  DW  ?
     .code
     include io.asm

fun   PROC
       push bp
       mov bp,sp
       sub sp,12

       mov ax,[BP+4]
       mov bx,[BP+6]
       imul bx
       mov [BP-4],ax

       mov ax,[BP-4]
       add ax,[BP+8]
       mov [BP-6],ax

       mov ax,[BP-6]
       mov [BP-2],ax

       mov dx, offset _S1
       call writestr

       mov ax,[BP-2]
       call writeint

       call writeln

       mov ax,0
       add sp,12
       pop bp
       ret 6
fun   ENDP

main   PROC
       push bp
       mov bp,sp
       sub sp,0

       mov ax,5
       mov a,ax

       mov ax,10
       mov b,ax

       mov ax,20
       mov d,ax

       mov ax,a
       push ax

       mov ax,d
       push ax

       mov ax,b
       push ax

       call fun
       mov a, ax

       mov ax,0
       add sp,0
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

