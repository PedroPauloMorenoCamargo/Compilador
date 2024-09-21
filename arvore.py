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
        #Lista de operações binárias
        operations = {
            'PLUS': lambda x, y: x + y,
            'MINUS': lambda x, y: x - y,
            'MULTIPLY': lambda x, y: x * y,
            'DIVIDE': lambda x, y: x // y,
            'GREATER': lambda x, y: x > y,
            'LESS': lambda x, y: x < y,
            'EQUALS': lambda x, y: x == y,
            'NOT_EQUALS': lambda x, y: x != y,
            'AND': lambda x, y: x and y,
            'OR': lambda x, y: x or y
        }
        #Se a operação estiver na lista de operações, executa a operação
        if self.value in operations:
            left = self.children[0].Evaluate(symbol_table)
            right = self.children[1].Evaluate(symbol_table)
            return operations[self.value](left, right)
    
        raise ValueError(f"Unknown Binary Operator: {self.value}")



class UnOp(Node):
    def __init__(self, value, child):
        super().__init__(value)
        self.children = [child]

    def Evaluate(self, symbol_table):
        operations = {
            'PLUS': lambda x: x,
            'MINUS': lambda x: -x,
            'NOT': lambda x: not x
        }

        if self.value in operations:
            child = self.children[0].Evaluate(symbol_table)
            return operations[self.value](child)
        raise ValueError(f"Unknown Unary operator: {self.value}")



class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self,symbol_table):
        #Retorna o valor do nó
        return self.value


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
        #Atribui o valor da expressão à variável
        symbol_table.set(self.children[0].value, self.children[1].Evaluate(symbol_table))


class Print(Node):
    def __init__(self, expression):
        super().__init__()
        self.children = [expression]

    def Evaluate(self, symbol_table):
        #Imprime o valor da expressão
        print(self.children[0].Evaluate(symbol_table))

class Scanf(Node):
    def __init__(self):
        super().__init__()

    def Evaluate(self, symbol_table):
        #Lê um valor do usuário
        value = int(input())
        return value  


class Statements(Node):
    def __init__(self):
        super().__init__()
        self.children = []

    def Evaluate(self, symbol_table):
        #Executa cada nó filho
        for child in self.children:
            child.Evaluate(symbol_table)

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
        #Se houver um bloco falso, adiciona ele à lista de filhos
        if false_block:
            self.children.append(false_block)

    def Evaluate(self, symbol_table):
        #Se a condição for verdadeira, executa o bloco verdadeiro caso contrário executa o bloco falso caso exista
        if self.children[0].Evaluate(symbol_table):
            self.children[1].Evaluate(symbol_table)
        elif len(self.children) == 3:
            self.children[2].Evaluate(symbol_table)

class While(Node):
    def __init__(self, condition, block):
        super().__init__()
        self.children = [condition, block]

    def Evaluate(self, symbol_table):
        #Enquanto a condição for verdadeira, executa o bloco
        while self.children[0].Evaluate(symbol_table):
            self.children[1].Evaluate(symbol_table)
