import re 
from arvore import *
class PrePro:
    @staticmethod
    def filter(source):
        # Remove C-style single-line (//) and multi-line (/* */) comments
        source = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)  # Remove multi-line comments
        # Remove spaces and newlines
        return ''.join(source)

class SymbolTable:
    def __init__(self):
        # Dicionário para armazenar as variáveis
        self.symbols = {}

    def get(self, name):
        # Retorna o valor da variável se ela existir caso contrário, levanta um erro
        if name in self.symbols:
            return self.symbols[name]
        else:
            raise ValueError(f"Undefined variable '{name}'")

    def set(self, name, value):
        # Define o valor da variável
        self.symbols[name] = value

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
        #Pula espaços e quebras de linha
        while self.position < len(self.source) and (self.source[self.position] == ' ' or self.source[self.position] == '\n'):
            self.position += 1
        #Verifica se chegou ao fim do código    
        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return
        
        caracter = self.source[self.position]

        #Determina o token
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
        elif caracter == '>':
            self.next = Token("GREATER", caracter)
        elif caracter == '<':
            self.next = Token("LESS", caracter)
        elif caracter == '=':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.position += 1
                self.next = Token("EQUALS", "==")
            else:
                self.next = Token("ASSIGN", caracter)
        elif caracter == '!':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.position += 1
                self.next = Token("NOT_EQUALS", "!=")
            else:
                self.next = Token("NOT", caracter)
        elif caracter == '&':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '&':
                self.position += 1
                self.next = Token("AND", "&&")
            else:
                raise ValueError("Invalid character: &")
        elif caracter == '|':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '|':
                self.position += 1
                self.next = Token("OR", "||")
            else:
                raise ValueError("Invalid character: |")
        elif caracter.isdigit():
            #Determina o número
            numero = self.source[self.position]
            while (self.position + 1) < len(self.source) and self.source[self.position + 1].isdigit():
                self.position += 1
                numero += self.source[self.position]
            self.next = Token("NUMBER", int(numero))
        elif caracter.isalpha():
            #Determina o identificador
            identificador = self.source[self.position]
            while (self.position + 1) < len(self.source) and (self.source[self.position + 1].isalnum() or self.source[self.position + 1] == '_'):
                self.position += 1
                identificador += self.source[self.position]
            #Verifica se é uma palavra reservada
            keywords = {
                "if": "IF",
                "else": "ELSE",
                "while": "WHILE",
                "scanf": "SCANF",
                "printf": "PRINTF"
            }
            if identificador in keywords:
                self.next = Token(keywords[identificador], identificador)
            else:
                self.next = Token("IDENTIFIER", identificador)
        else:
            raise ValueError(f"Invalid character: {caracter}")

        self.position += 1


class Parser:
    def __init__(self):
        self.tokenizer = None
        self.current_token = None

    def parseBlock(self):
        #Verifica se o bloco começa com chave esquerda
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'LBRACE':
            raise ValueError(f"Deveria receber chave esquerda no inicio do bloco mas recebeu: '{self.current_token.value}'")
        
        #Determina as declarações dentro do bloco
        self.tokenizer.selectNext()
        statements = Statements()
    
        while self.tokenizer.next.type != 'RBRACE' and self.tokenizer.next.type != 'EOF':
            statements.children.append(self.parseStatement())
        
        #Verifica se o bloco termina com chave direita
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'RBRACE':
            raise ValueError(f"Deveria receber chave direita no fim do bloco mas recebeu: '{self.current_token.value}'")
                
        return statements

    def parsePrintf(self):
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        #Verifica se o próximo token é um parênteses
        if self.current_token.type != 'LPAREN':
            raise ValueError(f"Deveria receber parênteses '(' após declaração da função printf, mas recebeu: '{self.current_token.value}'.")
        
        #Determina a expressão
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        expression = self.parseRelationalExpression()
        
        #Verifica se o próximo token é um parênteses
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'RPAREN':
            raise ValueError(f"Deveria receber parênteses ')' para fechar printf, mas recebeu: '{self.current_token.value}'.")
        
        return Print(expression)
    
    def parseIdentifier(self):
        #Determina o identificador
        id = self.tokenizer.next

        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        #Verifica se o próximo token é um '='
        if self.current_token.type != 'ASSIGN':
            raise ValueError(f"Deveria receber '=' após identificador, mas recebeu: '{self.current_token.value}'")
        
        #Determina a expressão
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        expression = self.parseRelationalExpression()

        return Assign(Identifier(id.value), expression)
    
    def parseIf(self):
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        #Verifica se o próximo token é um parênteses
        if self.current_token.type != 'LPAREN':
            raise ValueError(f"Deveria receber parênteses '(' após declaração da função if, mas recebeu: '{self.current_token.value}'.")
        
        #Determina a condição do if
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        condition = self.parseRelationalExpression()
        
        #Verifica se o próximo token é um parênteses
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'RPAREN':
            raise ValueError(f"Deveria receber parênteses ')' para fechar if, mas recebeu: '{self.current_token.value}'.")
        
        #Determina o bloco de código do if
        self.tokenizer.selectNext()
        true_block = self.parseStatement()
        
        #Verifica se existe um else
        self.current_token = self.tokenizer.next
        if self.current_token.type == 'ELSE':
            #Determina o bloco de código do else
            self.tokenizer.selectNext()
            false_block = self.parseStatement()
        else:
            false_block = None
        return If(condition, true_block, false_block)
    
    def parseWhile(self):
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        #Verifica se o próximo token é um parênteses
        if self.current_token.type != 'LPAREN':
            raise ValueError(f"Deveria receber parênteses '(' após declaração da função while, mas recebeu: '{self.current_token.value}'.")
        
        #Determina a condição do while
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        condition = self.parseRelationalExpression()
        
        #Verifica se o próximo token é um parênteses
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'RPAREN':
            raise ValueError(f"Deveria receber parênteses ')' para fechar while, mas recebeu: '{self.current_token.value}'.")
        
        #Determina o bloco de código do while
        self.tokenizer.selectNext()
        block = self.parseStatement()
        
        return While(condition, block)
    
    def parseStatement(self):
        self.current_token = self.tokenizer.next
        #Parse para printf ou identificador
        if self.current_token.type in ["PRINTF","IDENTIFIER"]:
            if self.current_token.type == "PRINTF":
                result = self.parsePrintf()
                self.tokenizer.selectNext()
            else:
                result = self.parseIdentifier()
            self.current_token = self.tokenizer.next
            if self.current_token.type != 'SEMICOLON':
                raise ValueError(f"Falta de ponto e vírgula após printf.")
        #Parase para ponto e vírgula
        elif self.current_token.type == 'SEMICOLON':
            result = NoOp()
        #Parse para bloco
        elif self.current_token.type == "LBRACE":
            result = self.parseBlock()
        #Parse para if
        elif self.current_token.type == "IF":
            return self.parseIf()
        #Parse para while
        elif self.current_token.type == "WHILE":
            return self.parseWhile()
        else:
            #Se não for nenhum dos anteriores, erro de sintaxe
            raise ValueError(f"Token inesperado: {self.current_token.value}")
        self.tokenizer.selectNext()
        return result

    def parseRelationalExpression(self):
        result = self.parseExpression()
        if self.current_token.type in ('GREATER', 'LESS', 'EQUALS', 'NOT_EQUALS'):
            operator = self.current_token.type
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            operand = self.parseExpression()
            result = BinOp(operator, result, operand)
        return result
    
    def parseExpression(self):
        result = self.parseTerm()
        while self.current_token.type in ('PLUS', 'MINUS', 'OR'):
            operator = self.current_token.type
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            operand = self.parseTerm()
            result = BinOp(operator, result, operand)
        return result
        
    def parseTerm(self):
        result = self.parseFactor()
        while self.current_token.type in ('MULTIPLY', 'DIVIDE', 'AND'):
            operator = self.current_token.type
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            operand = self.parseFactor()
            result = BinOp(operator, result, operand)
        return result
    
    def parseFactor(self):
        self.current_token = self.tokenizer.next
        token_type = self.current_token.type
        #Parse para número ou identificador
        if token_type in ["NUMBER", "IDENTIFIER"]:
            value = self.current_token.value
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            if self.current_token.type == token_type:
                raise ValueError(f"Erro de sintaxe: {token_type.lower()} depois de {token_type.lower()} '{self.current_token.value}'")
            return IntVal(value) if token_type == "NUMBER" else Identifier(value)
        #Parse para operador unário
        if token_type in ["PLUS", "MINUS", "NOT"]:
            self.tokenizer.selectNext()
            return UnOp(token_type, self.parseFactor())
        #Parse para scanf
        if token_type == "SCANF":
            self._parseScanf()
            return Scanf()
        #Parse para expressão entre parênteses
        if token_type == 'LPAREN':
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            result = self.parseRelationalExpression()
            if self.current_token.type != 'RPAREN':
                raise ValueError("Missing closing parenthesis")
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            return result

        raise ValueError(f"Caracter inválido: {token_type}")

    def _parseScanf(self):
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'LPAREN':
            raise ValueError(f"Expected '(' after 'scanf', got {self.current_token.value}")
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'RPAREN':
            raise ValueError(f"Expected ')' after 'scanf(', got {self.current_token.value}")
        self.tokenizer.selectNext()


    def run(self, code):
        #Inicializa Tokenizer
        self.tokenizer = Tokenizer(code)
        #Cria a AST
        ast = self.parseBlock()
        #Verifica se o código termina com EOF
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'EOF':
            raise ValueError(f"Erro de sintaxe: token inesperado '{self.current_token.value}' no final da expressão.")
        return ast

