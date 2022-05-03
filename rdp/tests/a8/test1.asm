     .model small
     .stack 100h
     .data
cc  DW  ?
a  DW  ?
b  DW  ?
     .code
     include io.asm

main   PROC
       push bp
       mov bp,sp
       sub sp,0

       mov ax,5
       mov a,ax

       mov ax,10
       mov b,ax

       mov ax,a
       mov bx,b
       imul bx
       mov [BP-2],ax

       mov ax,[BP-2]
       mov cc,ax

       mov ax,cc
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

