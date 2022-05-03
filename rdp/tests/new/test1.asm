     .model small
     .stack 100h
     .data
_S1  DB  "Enter a number between ","$"
_S2  DB  " and ","$"
_S3  DB  ": ","$"
_S4  DB  "You entered: ","$"
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
       add ax,[BP-4]
       mov [BP-8],ax

       mov ax,[BP-8]
       mov [BP-6],ax

       mov ax,[BP-2]
       mov bx,[BP-4]
       imul bx
       mov [BP-10],ax

       mov ax,[BP-10]
       mov [BP-6],ax

       mov ax,[BP-2]
       add ax,10
       mov [BP-12],ax

       mov ax,[BP-12]
       mov [BP-6],ax

       call main
       mov [BP-6], ax

       mov ax,0
       add sp,8
       pop bp
       ret 2
main   ENDP

_startproc    PROC
              mov ax, @data
              mov ds, ax
              call main
              mov ax, 4c00h
              int 21h
_startproc    ENDP
              END _startproc

