import sys

argumento = ''.join(sys.argv[1:])
argumento = argumento.replace(" ", "")

numero_final = 0
numero_atual = ""
operador_atual = "+"

for caracter in argumento:
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

if numero_atual:
    if operador_atual == "+":
        numero_final += int(numero_atual)
    elif operador_atual == "-":
        numero_final -= int(numero_atual)

print(numero_final)