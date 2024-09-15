from classes import *
import sys


if len(sys.argv) < 2:
    print("Uso: python3 parser.py <arquivo.c>")
    sys.exit(1)

filename = sys.argv[1]


with open(filename, 'r') as file:
    code = file.read()
    
filtered_code = PrePro.filter(code)
parser = Parser()
ast = parser.run(filtered_code)
symbol_table = SymbolTable()
if ast:
    ast.Evaluate(symbol_table)