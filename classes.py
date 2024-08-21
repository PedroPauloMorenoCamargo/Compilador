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
        elif caracter.isdigit():
            numero = self.source[self.position]
            while (self.position + 1) < len(self.source) and self.source[self.position + 1].isdigit():
                self.position += 1
                numero += self.source[self.position]
            self.next = Token("NUMBER", int(numero))
        else:
            raise ValueError("Caracter inválido")

        self.position += 1

class Parser:
    def __init__(self):
        self.tokenizer = None
        self.current_token = None
        self.operacao = False

    def parse_expression(self):
        result = self.parse_term()

        while self.current_token.type in ('PLUS', 'MINUS'):
            self.operacao = True
            operator = self.current_token.type
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            operand = self.parse_term()
            
            if operator == 'PLUS':
                result += operand
            elif operator == 'MINUS':
                result -= operand
        
        if not self.operacao:
            raise ValueError("Não há operadores na expressão")
        return result
    
    def parse_term(self):
        result = self.parse_factor()

        while self.current_token.type in ('MULTIPLY', 'DIVIDE'):
            operator = self.current_token.type
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            operand = self.parse_factor()
            
            if operator == 'MULTIPLY':
                result *= operand
            elif operator == 'DIVIDE':
                result /= operand

        return int(result)
    
    def parse_factor(self):
        self.current_token = self.tokenizer.next
        
        if self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            return value
        else:
            raise ValueError(f"Expected a number but got {self.current_token.type}")
        
    def run(self, code):
        self.tokenizer = Tokenizer(code)
        try:
            result = self.parse_expression()
        except ValueError as e:
            return str(e)
        return result
