import classes
import sys

if len(sys.argv) < 2:
    raise ValueError("Nenhum argumento passado")

argumento = ''.join(sys.argv[1:])
argumento = argumento.replace(" ", "")

tokenizer = classes.Tokenizer(argumento)
parser = classes.Parser(tokenizer)
print(parser.parse_expression())