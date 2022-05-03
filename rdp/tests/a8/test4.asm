     .model small
     .stack 100h
     .data
a  DW  ?
b  DW  ?
     .code
     include io.asm

double   PROC
       push bp
       mov bp,sp
       sub sp,6

       mov ax,[BP+4]
       mov [BP-2],ax

       mov ax,2
       mov bx,[BP+4]
       imul bx
       mov [BP-4],ax

       mov ax,[BP-4]
       mov [BP-2],ax

       mov ax,[BP-2]
       add sp,6
       pop bp
       ret 2
double   ENDP

main   PROC
       push bp
       mov bp,sp
       sub sp,0

       mov ax,5
       mov b,ax

       mov ax,b
       push ax

       call double
       mov a, ax

       mov ax,a
       call writeint

       call writeln

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

