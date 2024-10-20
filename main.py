from classes import *
import sys
from arvore import *

# Verifica se o arquivo foi passado como argumento
if len(sys.argv) < 2:
    print("Uso: python3 parser.py <arquivo.c>")
    sys.exit(1)

# Determina o nome do arquivo
filename = sys.argv[1]

#troca ".c" por ".asm"

file_out = filename.replace(".c", ".asm")

print(file_out)

# Lê o código do arquivo
with open(filename, 'r') as file:
    code = file.read()

# Filtra o código
filtered_code = PrePro.filter(code)

# Cria o parser
parser = Parser()

# Cria a árvore sintática
ast = parser.run(filtered_code)

# Cria a tabela de símbolos
symbol_table = SymbolTable()

# Cria uma lista para armazenar o código assembly gerado
assembly_code = []

# Create the LabelGenerator instance
label_generator = LabelGenerator()

# Avalia a árvore sintática e gera o código assembly
if ast:
    # Pass all the necessary arguments (assembly_code, symbol_table, label_counter)
    ast.Evaluate(assembly_code, symbol_table, label_generator)



# Assembly code header
assembly_header = """
SECTION .data
    ten     dd 10       ; Constant value 10

SECTION .bss
    number  resb 12     ; Buffer to store the string representation of the number

SECTION .text
    global main

main:
    PUSH EBP            ; Set up stack frame
    MOV EBP, ESP
"""

# Assembly code footer
assembly_footer = """
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
"""

# Função para escrever o código assembly gerado em um arquivo
def write_assembly_to_file(assembly_code, output_filename):
    # Write the assembly code to the file
    with open(output_filename, 'w') as asm_file:
        asm_file.write(assembly_header)
        for line in assembly_code:
            asm_file.write("    "+line + '\n')
        asm_file.write(assembly_footer)

# Escreve o código assembly gerado no arquivo
output_filename = file_out
write_assembly_to_file(assembly_code, output_filename)
