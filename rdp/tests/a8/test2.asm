     .model small
     .stack 100h
     .data
_S1  DB  "Enter a number ","$"
_S2  DB  "The answer is ","$"
a  DW  ?
b  DW  ?
     .code
     include io.asm

func   PROC
       push bp
       mov bp,sp
       sub sp,8

       mov dx, offset _S1
       call writestr

       call readint
       mov a, bx

       mov ax,10
       mov b,ax

       mov ax,20
       mov [BP-4],ax

       mov ax,a
       mov bx,b
       imul bx
       mov [BP-6],ax

       mov ax,[BP-4]
       add ax,[BP-6]
       mov [BP-8],ax

       mov ax,[BP-8]
       mov [BP-2],ax

       mov dx, offset _S2
       call writestr

       mov ax,[BP-2]
       call writeint

       call writeln

       mov ax,0
       add sp,8
       pop bp
       ret 0
func   ENDP

main   PROC
       push bp
       mov bp,sp
       sub sp,0

       call func
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

