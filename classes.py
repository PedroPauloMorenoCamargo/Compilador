class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        while self.position < len(self.source):
            current_char = self.source[self.position]
            if current_char.isdigit():
                self.tokens.append(self.create_number_token())
            elif current_char in '+-*/':
                self.tokens.append(Token('operator', current_char))
                self.position += 1
            else:
                raise ValueError(f"Invalid character found: {current_char}")
        
        self.tokens.append(Token('EOF', None))

    def create_number_token(self):
        start_position = self.position
        while self.position < len(self.source) and (self.source[self.position].isdigit()):
            self.position += 1
        value = int(self.source[start_position:self.position])
        return Token('number', value)

    def next_token(self):
        return self.tokens.pop(0) if self.tokens else None

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current_token = None

    def parse_expression(self):
        self.current_token = self.tokenizer.next_token()
        if self.current_token.type == 'EOF':
            raise ValueError("Empty expression")
        
        result = self.parse_term()
        while self.current_token and self.current_token.type == 'operator' and self.current_token.value in '+-':
            operator = self.current_token.value
            self.current_token = self.tokenizer.next_token()
            if self.current_token.type == 'EOF':
                raise ValueError("Expected a term after the operator but got EOF")
            
            operand = self.parse_term()
            if operator == '+':
                result += operand
            elif operator == '-':
                result -= operand
            
        return result

    def parse_term(self):
        if self.current_token.type == 'EOF':
            raise ValueError("Expected a number but got EOF")
        
        if self.current_token.type == 'number':
            value = self.current_token.value
            self.current_token = self.tokenizer.next_token()
            return value
        else:
            raise ValueError(f"Expected a number but got {self.current_token.type}")

    @staticmethod
    def run(code):
        tokenizer = Tokenizer(code)
        parser = Parser(tokenizer)
        try:
            result = parser.parse_expression()
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
