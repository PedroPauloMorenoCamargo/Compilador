
SECTION .data
    ten     dd 10       ; Constant value 10

SECTION .bss
    number  resb 12     ; Buffer to store the string representation of the number

SECTION .text
    global main

main:
    PUSH EBP            ; Set up stack frame
    MOV EBP, ESP
    MOV EBX, 555 ; Evaluate IntVal
    PUSH EBX ; Push the value to be printed onto the stack
    CALL print ; Call the print subroutine
    POP EBX ; Clean up the stack after the print

    MOV ESP, EBP        ; Clean up stack frame
    POP EBP
    MOV EAX, 1          ; sys_exit
    MOV EBX, 0          ; Exit code 0
    INT 0x80            ; Exit program

; Define the print subroutine
print:
    PUSH EBP
    MOV EBP, ESP
    PUSH EAX
    PUSH EBX
    PUSH ECX
    PUSH EDX

    ; Initialize pointers
    MOV ECX, number + 11 ; Point ECX to the end of the buffer
    MOV BYTE [ECX], 0    ; Null-terminate the string

    ; Move the number to EAX
    MOV EAX, EBX

    ; Check if number is zero
    CMP EAX, 0
    JNE print_check_sign
    ; Handle zero
    DEC ECX
    MOV BYTE [ECX], '0'
    JMP print_write

print_check_sign:
    ; Check if number is negative
    CMP EAX, 0
    JGE print_convert
    ; Handle negative number
    NEG EAX                ; Make EAX positive
    MOV BYTE [number], '-' ; Store the '-' sign
    MOV EBX, number        ; EBX points to the buffer start
    INC EBX                ; Move past the '-'
    JMP print_convert_setup

print_convert:
    MOV EBX, number        ; EBX points to the buffer start

print_convert_setup:
    ; Start converting digits
    DEC ECX

print_convert_loop:
    XOR EDX, EDX
    DIV DWORD [ten]        ; EAX = EAX / 10, EDX = remainder
    ADD EDX, '0'           ; Convert remainder to ASCII
    MOV [ECX], DL          ; Store character
    DEC ECX
    CMP EAX, 0
    JNE print_convert_loop

    INC ECX                ; Adjust ECX to point to the first digit

    ; Check if negative
    CMP BYTE [number], '-'
    JNE print_write_setup
    ; Adjust EBX to include '-'
    MOV EBX, number

print_write_setup:
    ; Adjust EDX to length of the string
    MOV EDX, number + 11
    SUB EDX, ECX           ; Length = end - start

print_write:
    ; Write the string to stdout
    MOV EAX, 4             ; sys_write
    MOV EBX, 1             ; stdout
    MOV ECX, ECX           ; Pointer to the string
    INT 0x80               ; Make the system call

    ; Restore registers
    POP EDX
    POP ECX
    POP EBX
    POP EAX
    MOV ESP, EBP
    POP EBP
    RET
