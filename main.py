import sys

if len(sys.argv) < 2:
    raise ValueError("Nenhum argumento passado")
argumento = ''.join(sys.argv[1:])
argumento = argumento.replace(" ", "")

numero_final = 0
numero_atual = ""
operador_atual = None
caracteres_validos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-'," "]
for caracter in argumento:
    if caracter not in caracteres_validos:
        raise ValueError("Caracter inválido")
    if caracter.isnumeric():
        numero_atual += caracter
    elif caracter == "+" or caracter == "-":
        if numero_atual:
            if operador_atual == "+":
                numero_final += int(numero_atual)
            elif operador_atual == "-":
                numero_final -= int(numero_atual)
            numero_atual = ""
            operador_atual = caracter
        else:
            raise ValueError("Operador sem número")

if operador_atual is None:
    raise ValueError("Operador não encontrado")

if numero_atual:
    if operador_atual == "+":
        numero_final += int(numero_atual)
    elif operador_atual == "-":
        numero_final -= int(numero_atual)