import sys
from abc import ABC, abstractmethod

import re 

class PrePro:
    @staticmethod
    def filter(source):
        # Remove C-style single-line (//) and multi-line (/* */) comments
        source = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)  # Remove multi-line comments
        # Remove spaces and newlines
        return ''.join(source)

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def get(self, name):
        if name in self.symbols:
            return self.symbols[name]
        else:
            raise ValueError(f"Undefined variable '{name}'")

    def set(self, name, value):
        self.symbols[name] = value



class Node(ABC):
    def __init__(self, value=None):
        self.value = value
        self.children = []

    @abstractmethod
    def Evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, value, left, right):
        super().__init__(value)
        self.children = [left, right]

    def Evaluate(self, symbol_table):
        if self.value == 'PLUS':
            return self.children[0].Evaluate(symbol_table) + self.children[1].Evaluate(symbol_table)
        elif self.value == 'MINUS':
            return self.children[0].Evaluate(symbol_table) - self.children[1].Evaluate(symbol_table)
        elif self.value == 'MULTIPLY':
            return self.children[0].Evaluate(symbol_table) * self.children[1].Evaluate(symbol_table)
        elif self.value == 'DIVIDE':
            return self.children[0].Evaluate(symbol_table) // self.children[1].Evaluate(symbol_table)


class UnOp(Node):
    def __init__(self, value, child):
        super().__init__(value)
        self.children = [child]

    def Evaluate(self, symbol_table):
        if self.value == 'PLUS':
            return self.children[0].Evaluate(symbol_table)
        elif self.value == 'MINUS':
            return -self.children[0].Evaluate(symbol_table)


class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self,symbol_table):
        return self.value


class Identifier(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self, symbol_table):
        return symbol_table.get(self.value)


class Assign(Node):
    def __init__(self, identifier, expression):
        super().__init__()
        self.children = [identifier, expression]

    def Evaluate(self, symbol_table):
        symbol_table.set(self.children[0].value, self.children[1].Evaluate(symbol_table))


class Print(Node):
    def __init__(self, expression):
        super().__init__()
        self.children = [expression]

    def Evaluate(self, symbol_table):
        print(self.children[0].Evaluate(symbol_table))

class Statements(Node):
    def __init__(self):
        super().__init__()
        self.children = []

    def Evaluate(self, symbol_table):
        for child in self.children:
            child.Evaluate(symbol_table)

class NoOp(Node):
    def __init__(self):
        super().__init__()

    def Evaluate(self,symbol_table):
        return 0    

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.selectNext()

    def selectNext(self):
        while self.position < len(self.source) and (self.source[self.position] == ' ' or self.source[self.position] == '\n'):
            self.position += 1
        
        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return
        
        caracter = self.source[self.position]

        if caracter == '+':
            self.next = Token("PLUS", caracter)
        elif caracter == '-':
            self.next = Token("MINUS", caracter)
        elif caracter == '*':
            self.next = Token("MULTIPLY", caracter)
        elif caracter == '/':
            self.next = Token("DIVIDE", caracter)
        elif caracter == '(':
            self.next = Token("LPAREN", caracter)
        elif caracter == ')':
            self.next = Token("RPAREN", caracter)
        elif caracter == ';':
            self.next = Token("SEMICOLON", caracter)
        elif caracter == '{':
            self.next = Token("LBRACE", caracter)
        elif caracter == '}':
            self.next = Token("RBRACE", caracter)
        elif caracter == "=":
            self.next = Token("EQUAL", caracter)
        elif caracter.isdigit():
            numero = self.source[self.position]
            while (self.position + 1) < len(self.source) and self.source[self.position + 1].isdigit():
                self.position += 1
                numero += self.source[self.position]
            self.next = Token("NUMBER", int(numero))
        elif caracter.isalpha():
            identificador = self.source[self.position]
            while (self.position + 1) < len(self.source) and (self.source[self.position + 1].isalnum() or self.source[self.position + 1] == '_'):
                self.position += 1
                identificador += self.source[self.position]
            if identificador == "printf":
                self.next = Token("PRINTF", identificador)
            else:
                self.next = Token("IDENTIFIER", identificador)
        else:
            raise ValueError(f"Caracter inválido: {caracter}")

        self.position += 1


class Parser:
    def __init__(self):
        self.tokenizer = None
        self.current_token = None

    def parseBlock(self):
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'LBRACE':
            raise ValueError(f"Deveria receber chave esquerda no inicio do bloco mas recebeu: '{self.current_token.value}'")
        
        self.tokenizer.selectNext()
        statements = Statements()

        while self.tokenizer.next.type != 'RBRACE' and self.tokenizer.next.type != 'EOF':
            statements.children.append(self.parseStatement())
            self.tokenizer.selectNext()

        self.current_token = self.tokenizer.next
        if self.current_token.type != 'RBRACE':
            raise ValueError(f"Deveria receber chave direita no fim do bloco mas recebeu: '{self.current_token.value}'")
                
        return statements

    def parsePrintf(self):
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'LPAREN':
            raise ValueError(f"Deveria receber parênteses '(' após declaração da função printf, mas recebeu: '{self.current_token.value}'.")
        
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        expression = self.parseExpression()
        
        self.current_token = self.tokenizer.next
        
        if self.current_token.type != 'RPAREN':
            raise ValueError(f"Deveria receber parênteses ')' para fechar printf, mas recebeu: '{self.current_token.value}'.")
        
        return Print(expression)
    

    def parseIdentifier(self):
        id = self.tokenizer.next

        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'EQUAL':
            raise ValueError(f"Deveria receber '=' após identificador, mas recebeu: '{self.current_token.value}'")
        
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        expression = self.parseExpression()

        return Assign(Identifier(id.value), expression)
    
    def parseStatement(self):
        self.current_token = self.tokenizer.next
        if self.current_token.type == 'PRINTF':
            result = self.parsePrintf()
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            if self.current_token.type != 'SEMICOLON':
                raise ValueError(f"Falta de ponto e vírgula após printf.")
        elif self.current_token.type == 'SEMICOLON':
            result = NoOp()
        elif self.current_token.type == 'IDENTIFIER':
            result = self.parseIdentifier()
            self.current_token = self.tokenizer.next
            if self.current_token.type != 'SEMICOLON':
                raise ValueError(f"Falta de ponto e vírgula após atribuição.")

        return result
        



    def parseExpression(self):
        result = self.parseTerm()
        while self.current_token.type in ('PLUS', 'MINUS'):
            operator = self.current_token.type
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            operand = self.parseTerm()
            result = BinOp(operator, result, operand)
        return result
        
    def parseTerm(self):
        result = self.parseFactor()
        while self.current_token.type in ('MULTIPLY', 'DIVIDE'):
            operator = self.current_token.type
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            operand = self.parseFactor()
            result = BinOp(operator, result, operand)
        return result
    
    def parseFactor(self):
        self.current_token = self.tokenizer.next
        if self.current_token.type == "NUMBER":
            value = self.current_token.value
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            if self.current_token.type == 'NUMBER':
                raise ValueError(f"Erro de sintaxe: número depois de numero '{self.current_token.value}'")
            return IntVal(value)
        elif self.current_token.type == "IDENTIFIER":
            value = self.current_token.value
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            if self.current_token.type == 'IDENTIFIER':
                raise ValueError(f"Erro de sintaxe: identificador depois de identificador '{self.current_token.value}'")
            return Identifier(value)
        elif self.current_token.type == "PLUS":
            self.tokenizer.selectNext()
            return UnOp("PLUS", self.parseFactor())
        elif self.current_token.type == "MINUS":
            self.tokenizer.selectNext()
            return UnOp("MINUS", self.parseFactor())
        elif self.current_token.type == 'LPAREN':
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            result = self.parseExpression()
            if self.current_token.type != 'RPAREN':
                raise ValueError("Missing closing parenthesis")
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            return result
        else:
            raise ValueError(f"Caracter invaliddo: {self.current_token.type}")
            

    def run(self, code):
        self.tokenizer = Tokenizer(code)
        ast = self.parseBlock()
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'EOF':
            raise ValueError(f"Erro de sintaxe: token inesperado '{self.current_token.value}' no final da expressão.")
        return ast

