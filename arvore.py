from abc import ABC, abstractmethod
#Superclasse de todos os nós da árvore
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
        left_value, left_type = self.children[0].Evaluate(symbol_table)
        right_value, right_type = self.children[1].Evaluate(symbol_table)

        if self.value == 'PLUS':
            if left_type == 'str' or right_type == 'str':
                
                return str(left_value) + str(right_value), 'str'
            return left_value + right_value, 'int'
        elif self.value == 'MINUS':
            if left_type == 'int' and right_type == 'int':
                return left_value - right_value, 'int'
            else:
                raise TypeError(f"Unsupported operands for '-': '{left_type}' and '{right_type}'")
        elif self.value == 'MULTIPLY':
            if left_type == 'int' and right_type == 'int':
                return left_value * right_value, 'int'
            else:
                raise TypeError(f"Unsupported operands for '*': '{left_type}' and '{right_type}'")
        elif self.value == 'DIVIDE':
            if left_type == 'int' and right_type == 'int':
                if right_value == 0:
                    raise ZeroDivisionError("Division by zero")
                return left_value // right_value, 'int'
            else:
                raise TypeError(f"Unsupported operands for '/': '{left_type}' and '{right_type}'")
        elif self.value == 'AND':
            if left_type != 'str' and right_type != 'str':
                return int(left_value and right_value), 'bool'
            else:
                raise TypeError(f"Unsupported operands for 'and': '{left_type}' and '{right_type}'")
        elif self.value == 'OR':
            if left_type != 'str' and right_type != 'str':
                return int(left_value or right_value), 'bool'
            else:
                raise TypeError(f"Unsupported operands for 'and': '{left_type}' and '{right_type}'")
        elif self.value == 'EQUALS':
            return int(left_value == right_value), 'bool'
        elif self.value == 'LESS':
            if left_type == right_type:
                return int(left_value < right_value), 'bool'
            elif (left_type == 'bool' and right_type == 'int') or (left_type == 'int' and right_type == 'bool'):
                return int(int(left_value) < int(right_value)), 'bool'
            else:
                raise TypeError(f"Cannot compare '{left_type}' and '{right_type}' with '<'")
        elif self.value == 'GREATER':
            if left_type == right_type:
                return int(left_value > right_value), 'bool'
            elif (left_type == 'bool' and right_type == 'int') or (left_type == 'int' and right_type == 'bool'):
                return int(int(left_value) > int(right_value)), 'bool'
            else:
                raise TypeError(f"Cannot compare '{left_type}' and '{right_type}' with '<'")
    
    
        raise ValueError(f"Unknown Binary Operator: {self.value}")



class UnOp(Node):
    def __init__(self, op, child):
        super().__init__(op)
        self.children = [child]

    def Evaluate(self, symbol_table):
        value, value_type = self.children[0].Evaluate(symbol_table)

        if self.value == 'PLUS':
            if value_type == 'int':
                return +value, 'int'
            else:
                raise TypeError(f"Unary '+' not supported for type '{value_type}'")

        elif self.value == 'MINUS':
            if value_type == 'int':
                return -value, 'int'
            else:
                raise TypeError(f"Unary '-' not supported for type '{value_type}'")

        elif self.value == 'NOT':
            if value_type == 'bool':
                return not value, 'bool'
            else:
                raise TypeError(f"Unary 'not' not supported for type '{value_type}'")

        else:
            raise ValueError(f"Unknown unary operator '{self.value}'")




class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self,symbol_table):
        #Retorna o valor do nó
        return self.value, 'int'
    
class StrVal(Node):
    def __init__(self, value):
        super().__init__(value.strip('"'))

    def Evaluate(self, symbol_table):
        return self.value, 'str'



class Identifier(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self, symbol_table):
        #Retorna o valor da variável
        return symbol_table.get(self.value)


class Assign(Node):
    def __init__(self, identifier, expression):
        super().__init__()
        self.children = [identifier, expression]

    def Evaluate(self, symbol_table):
        var_name = self.children[0].value
        # Check if the variable has been declared
        if var_name not in symbol_table.symbols:
            raise ValueError(f"Variable '{var_name}' not declared.")

        # Evaluate the expression
        value, value_type = self.children[1].Evaluate(symbol_table)
        expected_type = symbol_table.get(var_name)[1]

        # Type checking and implicit conversion if needed
        if value_type != expected_type:
            if expected_type == 'int' and value_type == 'bool':
                value = int(value)
                value_type = 'int'
            else:
                raise TypeError(f"Cannot assign '{value_type}' to '{expected_type}'.")

        # Assign the value and type to the variable in the symbol table
        symbol_table.set(var_name, (value, expected_type))
        return None, None  # Assignments do not return a value

class Declaration(Node):
    def __init__(self, var_type, declarations):
        super().__init__()
        self.var_type = var_type
        self.declarations = declarations

    def Evaluate(self, symbol_table):
        # Default values for each type
        default_values = {
            'int': 0,
            'str': ''
        }

        for var_name, expr in self.declarations:
            if var_name in symbol_table.symbols:
                raise ValueError(f"Variable '{var_name}' already declared.")

            if expr != None:
                # Evaluate the expression
                value, value_type = expr.Evaluate(symbol_table)

                # Type checking and implicit conversion
                if value_type != self.var_type:
                    if self.var_type == 'int' and value_type == 'bool':
                        value = int(value)
                        value_type = 'int'
                    else:
                        raise TypeError(f"Cannot assign '{value_type}' to '{self.var_type}'.")

                symbol_table.set(var_name, (value, self.var_type))
            else:
                # Assign default value
                symbol_table.set(var_name, (default_values[self.var_type], self.var_type))
        return None, None 


class Print(Node):
    def __init__(self, expression):
        super().__init__()
        self.children = [expression]

    def Evaluate(self, symbol_table):
        value, type = self.children[0].Evaluate(symbol_table)
        print(value)
        return None, None


class Scanf(Node):
    def __init__(self):
        super().__init__()

    def Evaluate(self, symbol_table):
        value = int(input())
        return value, 'int'



class Statements(Node):
    def __init__(self):
        super().__init__()
        self.children = []

    def Evaluate(self, symbol_table):
        for child in self.children:
            child.Evaluate(symbol_table)
        return None, None  # Statements do not return a value


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
        # If there's a false block, add it to the children
        if false_block:
            self.children.append(false_block)

    def Evaluate(self, symbol_table):
        condition_value, condition_type = self.children[0].Evaluate(symbol_table)
        if condition_type != 'bool':
            raise TypeError(f"Condition in 'if' must be 'bool', got '{condition_type}'")

        if condition_value:
            self.children[1].Evaluate(symbol_table)
        elif len(self.children) == 3:
            self.children[2].Evaluate(symbol_table)
        return None, None 

class While(Node):
    def __init__(self, condition, block):
        super().__init__()
        self.children = [condition, block]

    def Evaluate(self, symbol_table):
        while True:
            condition_value, condition_type = self.children[0].Evaluate(symbol_table)
            if condition_type != 'bool':
                raise TypeError(f"Condition in 'while' must be 'bool', got '{condition_type}'")
            if not condition_value:
                break
            self.children[1].Evaluate(symbol_table)
        return None, None  # While does not return a value

