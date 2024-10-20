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

# Cria um contador de labels
label_generator = Label_Generator()
# Avalia a árvore sintática e gera o código assembly
if ast:
    # Pass all the necessary arguments (assembly_code, symbol_table, label_counter)
    ast.Evaluate(assembly_code, symbol_table,label_generator)




# Assembly code header
assembly_header = """SECTION .data
    ten     dd 10
    newline db 10          ; Newline character (ASCII code 10)

SECTION .bss
    number  resb 12

SECTION .text
    global _start

_start:
    PUSH EBP
    MOV EBP, ESP
"""

assembly_footer = """    MOV ESP, EBP
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
