from abc import ABC, abstractmethod
#Superclasse de todos os nós da árvore
class Node(ABC):
    def __init__(self, value=None):
        self.value = value
        self.children = []

    @abstractmethod
    def Evaluate(self, assembly_code, symbol_table, label_generator):
        pass

class LabelGenerator:
    def __init__(self):
        self.counter = 0

    def get_label(self, prefix):
        label = f"{prefix}_{self.counter}"
        self.counter += 1
        return label


class BinOp(Node):
    def __init__(self, op, left, right):
        super().__init__(op)
        self.children = [left, right]

    def Evaluate(self, assembly_code, symbol_table, label_generator):
        # Evaluate the left side
        self.children[0].Evaluate(assembly_code, symbol_table, label_generator)
        assembly_code.append("PUSH EBX")

        # Evaluate the right side
        self.children[1].Evaluate(assembly_code, symbol_table, label_generator)
        assembly_code.append("POP EAX")

        #Realiza a operação
        if self.value == 'PLUS':
            #Adiciona o resultado ao lado esquerdo
            assembly_code.append("ADD EAX, EBX")  
        elif self.value == 'MINUS':
            #Subtrai o resultado do lado direito do lado esquerdo
            assembly_code.append("SUB EAX, EBX")  
        elif self.value == 'MULTIPLY':
            #Multiplica o resultado do lado direito pelo lado esquerdo
            assembly_code.append("IMUL EAX, EBX") 
        elif self.value == 'DIVIDE':
            #Limpa o registrador EDX
            assembly_code.append("MOV EDX, 0")
            #Realiza a divisão 
            assembly_code.append("DIV EBX")  

        # Guarda o resultado no registrador EBX
        assembly_code.append("MOV EBX, EAX")  
        
        return assembly_code




class UnOp(Node):
    def __init__(self, op, child):
        super().__init__(op)
        self.children = [child]

    def Evaluate(self, symbol_table):
        value, value_type = self.children[0].Evaluate(symbol_table)
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

    def Evaluate(self, assembly_code, symbol_table, label_generator):
        assembly_code.append(f"MOV EBX, {self.value} ; Evaluate IntVal")
    
class StrVal(Node):
    def __init__(self, value):
        super().__init__(value.strip('"'))
    
    def Evaluate(self, symbol_table):
        return self.value, 'str'



class Identifier(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self, assembly_code,symbol_table,label_generator):
        #Retorna o valor da variável
        return symbol_table.get(self.value)


class Assign(Node):
    def __init__(self, identifier, expression):
        super().__init__()
        self.children = [identifier, expression]

    def Evaluate(self, assembly_code, symbol_table, label_generator):
        var_name = self.children[0].value
        
        # Checa se a variável foi declarada
        if var_name not in symbol_table.symbols:
            raise ValueError(f"Variable '{var_name}' not declared.")

        # Avalia a expressão
        self.children[1].Evaluate(assembly_code, symbol_table, label_generator)  

        # Obtém o offset da variável na pilha
        offset = symbol_table.get_offset(var_name)

        # Armazena o valor da expressão na variável
        assembly_code.append(f"MOV [EBP-{offset}], EBX ; store the value in {var_name}")
        return assembly_code




class Declaration(Node):
    def __init__(self, var_type, declarations):
        super().__init__()
        self.var_type = var_type
        self.declarations = declarations

    def Evaluate(self, assembly_code, symbol_table, label_generator):
        # Valores padrão para inicialização de variáveis
        default_values = {
            'int': 0,
            'str': '' 
        }

        for var_name, expr in self.declarations:
            # Checa se a variável já foi declarada
            if var_name in symbol_table.symbols:
                raise ValueError(f"Variable '{var_name}' already declared.")
            
            # Declara a variável na tabela de símbolos
            symbol_table.declare(var_name, self.var_type)

            # Aloca espaço na pilha para a variável
            assembly_code.append(f"PUSH DWORD 0 ; allocate space for {var_name}")

            # Inicializa a variável com o valor da expressão (se houver)
            if expr is not None:
                # Avalia a expressão (que armazenará o resultado em EBX)
                expr.Evaluate(assembly_code, symbol_table, None)

                # Obtem o offset da variável na pilha
                offset = symbol_table.get_offset(var_name)

                # Guarda o valor da expressão na variável
                assembly_code.append(f"MOV [EBP-{offset}], EBX ; initialize {var_name} with the expression value")
            else:
                # Obtem o offset da variável na pilha
                offset = symbol_table.get_offset(var_name)
                default_value = default_values[self.var_type]
                # Inicializa a variável com um valor padrão
                assembly_code.append(f"MOV EBX, {default_value} ; default initialization for {var_name}")
                assembly_code.append(f"MOV [EBP-{offset}], EBX ; store default value in {var_name}")

        return assembly_code



class Print(Node):
    def __init__(self, expression):
        super().__init__()
        self.children = [expression]

    def Evaluate(self, assembly_code, symbol_table, label_generator):
        # Evaluate the expression (result in EBX)
        self.children[0].Evaluate(assembly_code, symbol_table, label_generator)  

        # Call the print subroutine
        assembly_code.append("CALL print ; Call the print subroutine")

        return assembly_code





class Statements(Node):
    def __init__(self):
        super().__init__()
        self.children = []

    def Evaluate(self, assembly_code, symbol_table, label_generator):
        # Avalia cada nó filho
        for child in self.children:
            child.Evaluate(assembly_code, symbol_table, label_generator)  
        return assembly_code




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
        if false_block:
            self.children.append(false_block)

    def Evaluate(self, assembly_code, symbol_table, label_generator):
        # Generate unique labels
        else_label = label_generator.get_label("ELSE")
        end_label = label_generator.get_label("END_IF")

        # Evaluate the condition
        self.children[0].Evaluate(assembly_code, symbol_table, label_generator)
        assembly_code.append("CMP EBX, 0 ; Check if the condition is false")
        assembly_code.append(f"JE {else_label} ; Jump to else if condition is false")

        # Evaluate the true block
        self.children[1].Evaluate(assembly_code, symbol_table, label_generator)
        assembly_code.append(f"JMP {end_label} ; Skip the else block")

        # Else block
        assembly_code.append(f"{else_label}: ; Else block start")
        if len(self.children) == 3:
            self.children[2].Evaluate(assembly_code, symbol_table, label_generator)

        # End of if statement
        assembly_code.append(f"{end_label}: ; End of the if statement")

class While(Node):
    def __init__(self, condition, block):
        super().__init__()
        self.children = [condition, block]

    def Evaluate(self, assembly_code, symbol_table, label_generator):
        # Generate unique labels
        start_label = label_generator.get_label("LOOP")
        end_label = label_generator.get_label("EXIT")

        # Start of the loop
        assembly_code.append(f"{start_label}: ; Start of the while loop")

        # Evaluate the condition
        self.children[0].Evaluate(assembly_code, symbol_table, label_generator)
        assembly_code.append("CMP EBX, 0 ; Check if the condition is false")
        assembly_code.append(f"JE {end_label} ; Jump to exit if the condition is false")

        # Evaluate the loop body
        self.children[1].Evaluate(assembly_code, symbol_table, label_generator)
        assembly_code.append(f"JMP {start_label} ; Jump back to the start of the loop")

        # End of the loop
        assembly_code.append(f"{end_label}: ; End of the while loop")

