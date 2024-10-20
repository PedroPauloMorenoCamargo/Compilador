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

# Função para escrever o código assembly gerado em um arquivo
def write_assembly_to_file(assembly_code, output_filename):
    with open(output_filename, 'w') as asm_file:
        for line in assembly_code:
            asm_file.write(line + '\n')

# Escreve o código assembly gerado no arquivo
output_filename = file_out
write_assembly_to_file(assembly_code, output_filename)
