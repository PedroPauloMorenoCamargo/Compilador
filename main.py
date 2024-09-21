from classes import *
import sys
from arvore import *

if len(sys.argv) < 2:
    print("Uso: python3 parser.py <arquivo.c>")
    sys.exit(1)

# Determina o nome do arquivo
filename = sys.argv[1]

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
# Avalia a árvore sintática
if ast:
    ast.Evaluate(symbol_table)