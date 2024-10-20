SECTION .data
    ten     dd 10
    newline db 10          ; Newline character (ASCII code 10)

SECTION .bss
    number  resb 12

SECTION .text
    global _start

_start:
    PUSH EBP
    MOV EBP, ESP
    PUSH DWORD 0
    MOV EBX, 0
    MOV DWORD [EBP-4], 0
    LOOP_1:
    MOV EBX, [EBP-4]
    PUSH EBX
    MOV EBX, 3
    POP EAX
    CMP EAX, EBX
    SETL AL
    MOVZX EBX, AL
    CMP EBX, 0
    JE EXIT_1
    MOV EBX, [EBP-4]
    PUSH EBX
    MOV EBX, 1
    POP EAX
    ADD EAX, EBX
    MOV EBX, EAX
    MOV [EBP-4], EBX
    JMP LOOP_1
    EXIT_1:
    MOV EBX, 4
    PUSH EBX
    MOV EBX, 0
    POP EAX
    CMP EAX, 0
    SETNE AL
    CMP EBX, 0
    SETNE BL
    AND AL, BL
    MOVZX EBX, AL
    CMP EBX, 0
    JE ELSE_2
    MOV EBX, 3
    PUSH EBX
    CALL print
    POP EBX
    JMP END_IF_2
    ELSE_2:
    MOV EBX, 0
    PUSH EBX
    CALL print
    POP EBX
    END_IF_2:
    MOV ESP, EBP
    POP EBP
    MOV EAX, 1     
    MOV EBX, 0       
    INT 0x80
print:
    PUSH EBP
    MOV EBP, ESP
    PUSH EAX
    PUSH EBX
    PUSH ECX
    PUSH EDX

    MOV ECX, number + 11     ; Point ECX to the end of the buffer
    MOV BYTE [ECX], 0        ; Null-terminate the string

    MOV EAX, EBX             ; EAX contains the value to print

    CMP EAX, 0
    JNE print_check_sign

    ; Handle zero case
    DEC ECX
    MOV BYTE [ECX], '0'
    JMP print_write_setup    ; Jump to print_write_setup instead of print_write

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
    ADD EDX, '0'             ; Convert digit to ASCII
    MOV [ECX], DL            ; Store digit in buffer
    DEC ECX
    CMP EAX, 0
    JNE print_convert_loop

    INC ECX

    CMP BYTE [number], '-'
    JNE print_write_setup

    MOV EBX, number

print_write_setup:
    MOV EDX, number + 11     ; EDX = address at the end of buffer
    SUB EDX, ECX             ; EDX = length of the string
    ; At this point, ECX points to the start of the string
    ; EDX contains the length of the string

print_write:
    MOV EAX, 4               ; sys_write
    MOV EBX, 1               ; stdout
    ; ECX already points to the buffer
    INT 0x80                 ; Make system call

    POP EDX
    POP ECX
    POP EBX
    POP EAX
    MOV ESP, EBP
    POP EBP
    RET


