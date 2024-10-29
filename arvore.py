from abc import ABC, abstractmethod

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

    def set(self, name, value_type):
        # Define o valor da variável
        self.symbols[name] = value_type
#Superclasse de todos os nós da árvore
class Node(ABC):
    def __init__(self, value=None):
        self.value = value
        self.children = []

    @abstractmethod
    def Evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, op, left, right):
        super().__init__(op)
        self.children = [left, right]

    def Evaluate(self, funct_table,symbol_table):
        left_value, left_type = self.children[0].Evaluate(funct_table,symbol_table)
        right_value, right_type = self.children[1].Evaluate(funct_table,symbol_table)
        #Possíveis operações binárias
        operations = {
            'PLUS': self._handle_plus,
            'MINUS': self._handle_minus,
            'MULTIPLY': self._handle_multiply,
            'DIVIDE': self._handle_divide,
            'AND': self._handle_and,
            'OR': self._handle_or,
            'EQUALS': self._handle_equals,
            'LESS': self._handle_less,
            'GREATER': self._handle_greater
        }
        #Verifica se a operação é válida
        if self.value in operations:
            return operations[self.value](left_value, left_type, right_value, right_type)
        else:
            raise ValueError(f"Unknown binary operator: {self.value}")
        
    #Funções que realizam as operações binárias
    def _handle_plus(self, left_value, left_type, right_value, right_type):
        if left_type == 'str' or right_type == 'str':
            return str(left_value) + str(right_value), 'str'
        return left_value + right_value, 'int'

    def _handle_minus(self, left_value, left_type, right_value, right_type):
        self._validate_type(left_type, right_type, 'int')
        return left_value - right_value, 'int'

    def _handle_multiply(self, left_value, left_type, right_value, right_type):
        self._validate_type(left_type, right_type, 'int')
        return left_value * right_value, 'int'

    def _handle_divide(self, left_value, left_type, right_value, right_type):
        self._validate_type(left_type, right_type, 'int')
        if right_value == 0:
            raise ZeroDivisionError("Division by zero")
        return left_value // right_value, 'int'

    def _handle_and(self, left_value, left_type, right_value, right_type):
        self._validate_not_str(left_type, right_type)
        return int(left_value and right_value), 'bool'

    def _handle_or(self, left_value, left_type, right_value, right_type):
        self._validate_not_str(left_type, right_type)
        return int(left_value or right_value), 'bool'

    def _handle_equals(self, left_value, left_type, right_value, right_type):
        if (left_type == 'str' and right_type != 'str') or (left_type != 'str' and right_type == 'str'):
            raise TypeError(f"Cannot compare 'str' with '{right_type}'")
        return int(left_value == right_value), 'bool'

    def _handle_less(self, left_value, left_type, right_value, right_type):
        self._validate_comparison(left_type, right_type)
        return int(left_value < right_value), 'bool'

    def _handle_greater(self, left_value, left_type, right_value, right_type):
        self._validate_comparison(left_type, right_type)
        return int(left_value > right_value), 'bool'

    def _validate_type(self, left_type, right_type, expected_type):
        if left_type != expected_type or right_type != expected_type:
            raise TypeError(f"Unsupported operands for operation: '{left_type}' and '{right_type}'")

    def _validate_not_str(self, left_type, right_type):
        if left_type == 'str' or right_type == 'str':
            raise TypeError(f"Unsupported operands for boolean operation: '{left_type}' and '{right_type}'")

    def _validate_comparison(self, left_type, right_type):
        if left_type != right_type and not ((left_type == 'bool' and right_type == 'int') or (left_type == 'int' and right_type == 'bool')):
            raise TypeError(f"Cannot compare '{left_type}' and '{right_type}'")




class UnOp(Node):
    def __init__(self, op, child):
        super().__init__(op)
        self.children = [child]

    def Evaluate(self,funct_table, symbol_table):
        value, value_type = self.children[0].Evaluate(funct_table,symbol_table)
        #Possíveis operações unárias
        operations = {
            'PLUS': self._handle_plus,
            'MINUS': self._handle_minus,
            'NOT': self._handle_not
        }
        #Verifica se a operação é válida
        if self.value in operations:
            return operations[self.value](value, value_type)
        else:
            raise ValueError(f"Unknown unary operator: {self.value}")
    #Funções que realizam as operações unárias
    def _handle_plus(self, value, value_type):
        self._validate_type(value_type, 'int')
        return +value, 'int'

    def _handle_minus(self, value, value_type):
        self._validate_type(value_type, 'int')
        return -value, 'int'

    def _handle_not(self, value, value_type):
        if value_type == 'bool' or value_type == 'int':
            return int(not value), 'bool'
        raise TypeError(f"Unary 'not' not supported for type '{value_type}'")

    def _validate_type(self, value_type, expected_type):
        if value_type != expected_type:
            raise TypeError(f"Unary operator not supported for type '{value_type}'")





class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self,funct_table,symbol_table):
        #Retorna o valor do nó
        return self.value, 'int'
    
class StrVal(Node):
    def __init__(self, value):
        super().__init__(value.strip('"'))
    
    def Evaluate(self, funct_table, symbol_table):
        return self.value, 'str'



class Identifier(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self, funct_table, symbol_table):
        #Retorna o valor da variável
        return symbol_table.get(self.value)


class Assign(Node):
    def __init__(self, identifier, expression):
        super().__init__()
        self.children = [identifier, expression]

    def Evaluate(self, funct_table, symbol_table):
        var_name = self.children[0].value
        # Checa se a variável foi declarada
        if var_name not in symbol_table.symbols:
            raise ValueError(f"Variable '{var_name}' not declared.")

        # Avalia a expressão
        value, value_type = self.children[1].Evaluate(funct_table, symbol_table)
        expected_type = symbol_table.get(var_name)[1]

        # Checagem de tipo e conversão implícita
        if value_type != expected_type:
            if expected_type == 'int' and value_type == 'bool':
                value = int(value)
                value_type = 'int'
            else:
                raise TypeError(f"Cannot assign '{value_type}' to '{expected_type}'.")

        # Atribui o valor à variável
        symbol_table.set(var_name, (value, expected_type))
        return None, None 

class Declaration(Node):
    def __init__(self, var_type, declarations):
        super().__init__()
        self.var_type = var_type
        self.declarations = declarations

    def Evaluate(self, funct_table, symbol_table):
        # Valores padrão para inicialização
        default_values = {
            'int': 0,
            'str': ''
        }

        for var_name, expr in self.declarations:
            # Checa se a variável já foi declarada
            if var_name in symbol_table.symbols:
                raise ValueError(f"Variable '{var_name}' already declared.")
            
            if expr != None:
                # Avalia a expressão
                value, value_type = expr.Evaluate(symbol_table)

                # Checagem de tipo e conversão implícita
                if value_type != self.var_type:
                    if self.var_type == 'int' and value_type == 'bool':
                        value = int(value)
                        value_type = 'int'
                    else:
                        raise TypeError(f"Cannot assign '{value_type}' to '{self.var_type}'.")
                # Atribui o valor à variável
                symbol_table.set(var_name, (value, self.var_type))
            else:
                # Atribui o valor padrão à variável
                symbol_table.set(var_name, (default_values[self.var_type], self.var_type))
        return None, None 


class Print(Node):
    def __init__(self, expression):
        super().__init__()
        self.children = [expression]

    def Evaluate(self, funct_table, symbol_table):
        value, type = self.children[0].Evaluate(funct_table, symbol_table)
        print(value)
        return None, None


class Scanf(Node):
    def __init__(self):
        super().__init__()

    def Evaluate(self, funct_table, symbol_table):
        # Lê um valor int do usuário
        value = int(input())
        return value, 'int'



class Statements(Node):
    def __init__(self):
        super().__init__()
        self.children = []

    def Evaluate(self,funct_table,  symbol_table):
        # Avalia cada nó filho
        for child in self.children:
            child.Evaluate(funct_table, symbol_table)
        return None, None  


class NoOp(Node):
    def __init__(self):
        super().__init__()

    def Evaluate(self,symbol_table):
        #Faz nada
        return 0    
    

class If(Node):
    def __init__(self, condition, true_block, false_block=None):
        super().__init__()
        self.children = [condition, true_block]
        # Se houver um bloco 'else'
        if false_block:
            self.children.append(false_block)

    def Evaluate(self, funct_table, symbol_table):
        condition_value, condition_type = self.children[0].Evaluate(funct_table, symbol_table)
        # Checa se a condição é do tipo 'bool'
        if condition_type != 'bool':
            raise TypeError(f"Condition in 'if' must be 'bool', got '{condition_type}'")
        # Avalia o bloco correspondente
        if condition_value:
            self.children[1].Evaluate(funct_table, symbol_table)
        elif len(self.children) == 3:
            self.children[2].Evaluate(funct_table, symbol_table)
        return None, None 

class While(Node):
    def __init__(self, condition, block):
        super().__init__()
        self.children = [condition, block]

    def Evaluate(self, funct_table, symbol_table):
        while True:
            condition_value, condition_type = self.children[0].Evaluate(funct_table, symbol_table)
            # Checa se a condição é do tipo 'bool'
            if condition_type != 'bool':
                raise TypeError(f"Condition in 'while' must be 'bool', got '{condition_type}'")
            # Avalia a condição para continuar ou não
            if not condition_value:
                break
            self.children[1].Evaluate(funct_table, symbol_table)
        return None, None  



class Program(Node):
    def __init__(self):
        super().__init__()
        self.children = []

    def Evaluate(self, func_table,symbol_table):
        for child in self.children:
            child.Evaluate(func_table,symbol_table)
        return None, None

class FuncDecl(Node):
    def __init__(self, func_type, func_name, args, block):
        super().__init__()
        self.func_type = func_type
        self.func_name = func_name
        self.params = args
        self.children = [block]

    def Evaluate(self,func_table,symbol_table):
        # Checa se a função já foi declarada
        if self.func_name in func_table.functions:
            raise ValueError(f"Function '{self.func_name}' already declared.")
        # Adiciona a função à tabela de símbolos
        func_table.set(self.func_name, self)
        return None, None
    
class FuncCall(Node):
    def __init__(self, func_name, args):
        super().__init__()
        self.func_name = func_name
        self.children = args

    def Evaluate(self, func_table, symbol_table):
        # Pegar a função da tabela de funções
        func_dec = func_table.get(self.func_name)
        func_params = func_dec.params
        func_block = func_dec.children[0]
        if len(self.children) != len(func_params):
            raise ValueError(f"Function '{self.func_name}' expects {len(func_params)} arguments, got {len(self.children)}.")
        # Evaluate arguments
        args_values = []
        for arg in self.children:
            val, val_type = arg.Evaluate(func_table, symbol_table)
            args_values.append((val, val_type))
        # Criar uma nova tabela de símbolos para a função
        func_symbol_table = SymbolTable()
        # Inicializar os parâmetros da função no novo escopo
        for (param_type, param_name), (arg_value, arg_type) in zip(func_params, args_values):
            if param_type != arg_type:
                # Conversão implícita de bool para int
                if param_type == 'int' and arg_type == 'bool':
                    arg_value = int(arg_value)
                else:
                    raise TypeError(f"Type mismatch in function '{self.func_name}' argument '{param_name}': expected '{param_type}', got '{arg_type}'.")
            func_symbol_table.set(param_name, (arg_value, param_type))
        # Executa o bloco da função
        try:
            func_block.Evaluate(func_table, func_symbol_table)
            if func_dec.func_type != 'void' and self.func_name != 'main':
                raise ValueError(f"Function '{self.func_name}' should return a value.")
            else:
                return None, None
        except ReturnException as e:
            if func_dec.func_type == 'void' and self.func_name != 'main':
                raise ValueError(f"Function '{self.func_name}' should not return a value.")
            return e.value, e.value_type


class ReturnException(Exception):
    def __init__(self, value, value_type):
        self.value = value
        self.value_type = value_type

class Return(Node):
    def __init__(self, expression):
        super().__init__()
        self.children = [expression]

    def Evaluate(self, func_table, symbol_table):
        value, value_type = self.children[0].Evaluate(func_table, symbol_table)
        raise ReturnException(value, value_type)
