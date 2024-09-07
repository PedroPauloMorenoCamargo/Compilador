import sys
from abc import ABC, abstractmethod

import re 

class PrePro:
    @staticmethod
    def filter(source):
        # Remove C-style single-line (//) and multi-line (/* */) comments
        source = re.sub(r'//.*', '', source)  # Remove single-line comments
        source = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)  # Remove multi-line comments
        
        # Remove spaces and newlines
        return ''.join(source).replace(' ', '').replace('\n', '')


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

    def Evaluate(self):
        if self.value == 'PLUS':
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == 'MINUS':
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif self.value == 'MULTIPLY':
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif self.value == 'DIVIDE':
            return self.children[0].Evaluate() // self.children[1].Evaluate()

class UnOp(Node):
    def __init__(self, value, child):
        super().__init__(value)
        self.children = [child]

    def Evaluate(self):
        if self.value == 'PLUS':
            return self.children[0].Evaluate()
        elif self.value == 'MINUS':
            return -self.children[0].Evaluate()

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self):
        return self.value

class NoOp(Node):
    def Evaluate(self):
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
        while self.position < len(self.source) and self.source[self.position] == ' ':
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
        elif caracter.isdigit():
            numero = self.source[self.position]
            while (self.position + 1) < len(self.source) and self.source[self.position + 1].isdigit():
                self.position += 1
                numero += self.source[self.position]
            self.next = Token("NUMBER", int(numero))
        else:
            raise ValueError(f"Caracter inválido: {caracter}")

        self.position += 1


class Parser:
    def __init__(self):
        self.tokenizer = None
        self.current_token = None
        self.op = False

    def parseExpression(self):
        result = self.parseTerm()
        while self.current_token.type in ('PLUS', 'MINUS'):
            self.op = True
            operator = self.current_token.type
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            operand = self.parseTerm()
            result = BinOp(operator, result, operand)
        return result
    
    def parseTerm(self):
        result = self.parseFactor()
        while self.current_token.type in ('MULTIPLY', 'DIVIDE'):
            self.op = True
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
            return IntVal(value)
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
            raise ValueError(f"Expected a number or parenthesis but got {self.current_token.type}")
        
    def run(self, code):
        self.tokenizer = Tokenizer(code)
        ast = self.parseExpression()
        if not self.op:
            raise ValueError("Erro de sintaxe: expressão sem Operador.")
        if self.current_token.type != 'EOF':
            raise ValueError(f"Erro de sintaxe: token inesperado '{self.current_token.value}' no final da expressão.")
        return ast

