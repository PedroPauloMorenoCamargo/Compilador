import re 
from arvore import *
class PrePro:
    @staticmethod
    def filter(source):
        # Remove C-style single-line (//) and multi-line (/* */) comments
        source = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)  # Remove multi-line comments
        # Remove spaces and newlines
        return ''.join(source)


class FuncTable:
    functions = {}

    @staticmethod
    def set(name, func_node):
        if name in FuncTable.functions:
            raise ValueError(f"Function '{name}' already declared.")
        FuncTable.functions[name] = func_node

    @staticmethod
    def get(name):
        if name not in FuncTable.functions:
            raise ValueError(f"Function '{name}' not declared.")
        return FuncTable.functions[name]


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
        elif caracter == ',':
            self.next = Token("COMMA", caracter)
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
        elif caracter == '"':
            #Determina a string
            string = ""
            self.position += 1
            while self.position < len(self.source) and self.source[self.position] != '"':
                string += self.source[self.position]
                self.position += 1
            if self.position >= len(self.source):
                raise ValueError("String not closed")
            self.next = Token("STRING", string)
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
                "printf": "PRINTF",
                "int": "TYPE",
                "str": "TYPE",
                "void": "FUNC_TYPE",
                "return": "RETURN"
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

    def parseProgram(self):
        functions = Program()
        #Loopa Até o fim do código
        while self.tokenizer.next.type != 'EOF':
            #Pega a função
            functions.children.append(self.parseFunction())
            self.tokenizer.selectNext()
        #Chama a função main
        functions.children.append(FuncCall("main", []))
        return functions
    
    def parseFunction(self):
        #Verifica se a função tem tipo
        if self.tokenizer.next.type != 'TYPE' and self.tokenizer.next.type != 'FUNC_TYPE':
            raise ValueError(f"Expected 'TYPE' initializing the function, got {self.tokenizer.next.value}")
        function_type = self.tokenizer.next.value
        #Verifica se a função tem nome
        self.tokenizer.selectNext()
        if self.tokenizer.next.type != 'IDENTIFIER':
            raise ValueError(f"Expected function name after 'TYPE', got {self.tokenizer.next.value}")
        function_name = self.tokenizer.next.value
        #Verifica se a função tem paranteses esquerdo
        self.tokenizer.selectNext()
        if self.tokenizer.next.type != 'LPAREN':
            raise ValueError(f"Expected '(' after function name, got {self.tokenizer.next.value}")
        self.tokenizer.selectNext()
        #Cria a lista de parâmetros
        params = []
        while self.tokenizer.next.type != 'RPAREN':
            if self.tokenizer.next.type != 'TYPE':
                raise ValueError(f"Expected 'TYPE' after '(', got {self.tokenizer.next.value}")
            param_type = self.tokenizer.next.value
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != 'IDENTIFIER':
                raise ValueError(f"Expected parameter name after 'TYPE', got {self.tokenizer.next.value}")
            param_name = self.tokenizer.next.value
            params.append((param_type, param_name))
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == 'COMMA':
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == 'RPAREN':
                    raise ValueError(f"Expected parameter after comma, got {self.tokenizer.next.value}")
        #Pega o bloco de código da função
        self.tokenizer.selectNext()
        block = self.parseBlock()
        #Cria o nó da função
        func_dec = FuncDecl(function_type, function_name, params, block)
        return func_dec


    def parseBlock(self):
        #Verifica se o bloco começa com chave esquerda
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'LBRACE':
            raise ValueError(f"Deveria receber chave esquerda no inicio do bloco mas recebeu: '{self.current_token.value}'")
        
        #Determina as declarações dentro do bloco
        self.tokenizer.selectNext()
        statements = Statements()
    
        while self.tokenizer.next.type != 'RBRACE':
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
    
    def parseIdentifierOrFuncCall(self):
        # Determina o identificador
        id_token = self.tokenizer.next
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        # Realiza a verificação se é uma atribuição ou uma chamada de função
        if self.current_token.type == 'ASSIGN':
            self.tokenizer.selectNext()
            expression = self.parseRelationalExpression()
            return Assign(Identifier(id_token.value), expression)
        elif self.current_token.type == 'LPAREN':
            self.tokenizer.selectNext()
            args = []
            while self.tokenizer.next.type != 'RPAREN':
                arg_expr = self.parseRelationalExpression()
                args.append(arg_expr)
                if self.tokenizer.next.type == 'COMMA':
                    self.tokenizer.selectNext()
            self.tokenizer.selectNext() 
            return FuncCall(id_token.value, args)
        else:
            raise ValueError(f"Token Inesperado depois de identificador '{id_token.value}': '{self.current_token.value}'")

    
    def parseDeclaration(self):
        #Determina o tipo da variável
        var_type = self.tokenizer.next.value
        self.tokenizer.selectNext()
        #Lista das declarações
        declarations = []

        while True:
            #Determina o identificador
            identifier = self.tokenizer.next
            self.tokenizer.selectNext()
            #Verifica se o próximo token é uma vírgula e continua a declaração
            if self.tokenizer.next.type == 'COMMA':
                declarations.append((identifier.value, None))
                self.tokenizer.selectNext()
                continue
            #Verifica se o próximo token é um '='
            if self.tokenizer.next.type == 'ASSIGN':
                self.tokenizer.selectNext()
                expression = self.parseRelationalExpression()
                declarations.append((identifier.value, expression))
                #Verifica se o próximo token é uma vírgula e continua a declaração
                if self.tokenizer.next.type == 'COMMA':
                    self.tokenizer.selectNext()
                    continue
                #Verifica se o próximo token é um ponto e vírgula e finaliza a declaração
                elif self.tokenizer.next.type == 'SEMICOLON':
                    break
                else:
                    raise ValueError(f"Erro de sintaxe: {self.tokenizer.next.value}")
            #Verifica se o próximo token é um ponto e vírgula e finaliza a declaração
            elif self.tokenizer.next.type == 'SEMICOLON':
                declarations.append((identifier.value, None))
                break

            else:
                raise ValueError(f"Erro de sintaxe: {self.tokenizer.next.value}")
        #Cria o nó de declaração
        declaration_node = Declaration(var_type, declarations)
        return declaration_node



        

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
    
    def parseReturn(self):
        self.tokenizer.selectNext()
        expression = self.parseRelationalExpression()
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'SEMICOLON':
            raise ValueError("Missing semicolon after return statement.")
        self.tokenizer.selectNext()
        return Return(expression)


    def parseStatement(self):
        self.current_token = self.tokenizer.next
        #Parse para print, atribuição ou declaração
        if self.current_token.type in ["PRINTF", "IDENTIFIER", "TYPE"]:
            if self.current_token.type == "PRINTF":
                result = self.parsePrintf()
                self.tokenizer.selectNext()
            elif self.current_token.type == "IDENTIFIER":
                result = self.parseIdentifierOrFuncCall()
            elif self.current_token.type == "TYPE":
                result = self.parseDeclaration()
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
        #Parse para return
        elif self.current_token.type == "RETURN":
            return self.parseReturn()
        else:
            #Se não for nenhum dos anteriores, erro de sintaxe
            raise ValueError(f"Token inesperado: {self.current_token.value}")
        self.tokenizer.selectNext()
        return result

    def parseRelationalExpression(self):
        #Determina a expressão
        result = self.parseExpression()
        #Verifica se o próximo token é um operador relacional
        if self.current_token.type in ('GREATER', 'LESS', 'EQUALS', 'NOT_EQUALS'):
            #Determina o operador relacional
            operator = self.current_token.type
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            #Determina a proxima expressão
            operand = self.parseExpression()
            #Cria o nó da expressão relacional
            result = BinOp(operator, result, operand)
        return result
    
    def parseExpression(self):
        #Determina o termo
        result = self.parseTerm()
        #Verifica se o próximo token é um operador de Expressão
        while self.current_token.type in ('PLUS', 'MINUS', 'OR'):
            #Determina o operador de Expressão
            operator = self.current_token.type
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            #Determina o próximo termo
            operand = self.parseTerm()
            #Cria o nó da expressão
            result = BinOp(operator, result, operand)
        return result
        
    def parseTerm(self):
        #Determina o fator
        result = self.parseFactor()
        #Verifica se o próximo token é um operador de Termo
        while self.current_token.type in ('MULTIPLY', 'DIVIDE', 'AND'):
            #Determina o operador de Termo
            operator = self.current_token.type
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            #Determina o próximo fator
            operand = self.parseFactor()
            #Cria o nó do termo
            result = BinOp(operator, result, operand)
        return result
    
    def parseFactor(self):
        self.current_token = self.tokenizer.next
        token_type = self.current_token.type

        if token_type == 'IDENTIFIER':
            identifier_name = self.current_token.value
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            if self.current_token.type == 'LPAREN':
                # Function call with return value
                self.tokenizer.selectNext()
                args = []
                while self.tokenizer.next.type != 'RPAREN':
                    arg_expr = self.parseRelationalExpression()
                    args.append(arg_expr)
                    if self.tokenizer.next.type == 'COMMA':
                        self.tokenizer.selectNext()
                self.tokenizer.selectNext()
                self.current_token = self.tokenizer.next
                return FuncCall(identifier_name, args)
            else:
                return Identifier(identifier_name)

        #Parse para número ou string
        if token_type in ["NUMBER", "STRING"]:
            value = self.current_token.value
            self.tokenizer.selectNext()
            self.current_token = self.tokenizer.next
            if self.current_token.type == token_type:
                raise ValueError(f"Erro de sintaxe: {token_type.lower()} depois de {token_type.lower()} '{self.current_token.value}'")
            if token_type == "NUMBER":
                return IntVal(value)
            elif token_type == "STRING":
                return StrVal(value)
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
        ast = self.parseProgram()
        #Verifica se o código termina com EOF
        self.tokenizer.selectNext()
        self.current_token = self.tokenizer.next
        if self.current_token.type != 'EOF':
            raise ValueError(f"Erro de sintaxe: token inesperado '{self.current_token.value}' no final da expressão.")
        return ast

