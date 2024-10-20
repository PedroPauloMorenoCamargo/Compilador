
SECTION .data
    ten     dd 10       ; Constant value 10

SECTION .bss
    number  resb 12     ; Buffer to store the string representation of the number

SECTION .text
    global main

main:
    PUSH EBP            ; Set up stack frame
    MOV EBP, ESP
    PUSH DWORD 0 ; allocate space for x
    MOV EBX, 0 ; default initialization for x
    MOV [EBP-4], EBX ; store default value in x
    MOV EBX, 10 ; Evaluate IntVal
    MOV [EBP-4], EBX ; store the value in x
    PUSH DWORD 0 ; allocate space for y
    MOV EBX, 0 ; default initialization for y
    MOV [EBP-8], EBX ; store default value in y
    PUSH EBX
    MOV EBX, 5 ; Evaluate IntVal
    POP EAX
    SUB EAX, EBX
    MOV EBX, EAX
    MOV [EBP-8], EBX ; store the value in y

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

    ; Convert integer in EBX to string
    MOV EAX, EBX        ; Move the integer to EAX for division
    MOV ECX, number + 11 ; Point ECX to the end of the buffer
    MOV BYTE [ECX], 0    ; Null-terminate the string
    DEC ECX              ; Move to the previous character

    ; Handle zero case
    CMP EAX, 0
    JNE print_loop
    MOV BYTE [ECX], '0'
    DEC ECX
    JMP print_end_loop

print_loop:
    XOR EDX, EDX
    DIV DWORD [ten]      ; Divide EAX by 10
    ADD EDX, '0'         ; Convert remainder to ASCII
    MOV [ECX], DL        ; Store character in buffer
    DEC ECX
    CMP EAX, 0
    JNE print_loop

print_end_loop:
    INC ECX              ; Move ECX to the start of the string

    ; Write the string to stdout
    MOV EAX, 4           ; sys_write
    MOV EBX, 1           ; stdout
    MOV EDX, number + 11 ; End of buffer
    SUB EDX, ECX         ; Length of the string
    MOV ECX, ECX         ; Pointer to the string
    INT 0x80             ; Make the system call

    ; Restore registers
    POP EDX
    POP ECX
    POP EBX
    POP EAX
    MOV ESP, EBP
    POP EBP
    RET
