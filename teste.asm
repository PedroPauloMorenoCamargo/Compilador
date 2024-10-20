
SECTION .data
    ten     dd 10

SECTION .bss
    number  resb 12

SECTION .text
    global main

main:
    PUSH EBP
    MOV EBP, ESP
    MOV EBX, 5 ; Evaluate IntVal
    PUSH EBX
    MOV EBX, 2 ; Evaluate IntVal
    POP EAX
    MOV EBX, EAX
    CALL print ; Call the print subroutine

print:
    PUSH EBP
    MOV EBP, ESP
    PUSH EAX
    PUSH EBX
    PUSH ECX
    PUSH EDX

    MOV ECX, number + 11
    MOV BYTE [ECX], 0

    MOV EAX, EBX

    CMP EAX, 0
    JNE print_check_sign

    DEC ECX
    MOV BYTE [ECX], '0'
    JMP print_write

print_check_sign:
    CMP EAX, 0
    JGE print_convert

    NEG EAX
    MOV BYTE [number], '-'
    MOV EBX, number
    INC EBX
    JMP print_convert_setup

print_convert:
    MOV EBX, number

print_convert_setup:
    DEC ECX

print_convert_loop:
    XOR EDX, EDX
    DIV DWORD [ten]
    ADD EDX, '0'
    MOV [ECX], DL
    DEC ECX
    CMP EAX, 0
    JNE print_convert_loop

    INC ECX

    CMP BYTE [number], '-'
    JNE print_write_setup

    MOV EBX, number

print_write_setup:
    MOV EDX, number + 11
    SUB EDX, ECX

print_write:
    MOV EAX, 4
    MOV EBX, 1
    MOV ECX, ECX
    INT 0x80

    POP EDX
    POP ECX
    POP EBX
    POP EAX
    MOV ESP, EBP
    POP EBP
    RET
