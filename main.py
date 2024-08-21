from classes import Parser
import sys

if len(sys.argv) < 2:
    raise ValueError("Nenhum argumento passado")

argumento = ''.join(sys.argv[1:])
argumento = argumento.replace(" ", "")

parser = Parser()
print(parser.run(argumento))