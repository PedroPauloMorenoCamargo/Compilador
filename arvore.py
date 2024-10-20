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
    def __init__(self, op, left, right):
        super().__init__(op)
        self.children = [left, right]

    def Evaluate(self, assembly_code, symbol_table, label_generator):
        # Evaluate left operand
        left_value, left_type = self.children[0].Evaluate(assembly_code, symbol_table, label_generator)
        assembly_code.append(f"PUSH EBX")  # Save left operand (EBX)
        # Evaluate right operand
        right_value, right_type = self.children[1].Evaluate(assembly_code, symbol_table, label_generator)
        assembly_code.append(f"POP EAX")   # Retrieve left operand into EAX
        # Now, EAX = left operand, EBX = right operand

        if self.value == "PLUS":
            assembly_code.append(f"ADD EAX, EBX")  # EAX = EAX + EBX
            assembly_code.append(f"MOV EBX, EAX")  # Move result to EBX
        elif self.value == "MINUS":
            assembly_code.append(f"SUB EAX, EBX")  # EAX = EAX - EBX
            assembly_code.append(f"MOV EBX, EAX")  # Move result to EBX
        elif self.value == "EQUALS":
            assembly_code.append(f"CMP EAX, EBX")  # Compare EAX and EBX
            assembly_code.append(f"SETE AL")       # AL = 1 if EAX == EBX
            assembly_code.append(f"MOVZX EBX, AL") # Zero-extend AL into EBX
        elif self.value == "GREATER":
            assembly_code.append(f"CMP EAX, EBX")  # Compare EAX and EBX
            assembly_code.append(f"SETG AL")       # AL = 1 if EAX > EBX
            assembly_code.append(f"MOVZX EBX, AL") # Zero-extend AL into EBX
        elif self.value == "LESS":
            assembly_code.append(f"CMP EAX, EBX")  # Compare EAX and EBX
            assembly_code.append(f"SETL AL")       # AL = 1 if EAX < EBX
            assembly_code.append(f"MOVZX EBX, AL") # Zero-extend AL into EBX
        elif self.value == "AND":
            assembly_code.append(f"CMP EAX, 0")    # Check if EAX is not zero
            assembly_code.append(f"SETNE AL")      # AL = 1 if EAX != 0
            assembly_code.append(f"CMP EBX, 0")    # Check if EBX is not zero
            assembly_code.append(f"SETNE BL")      # BL = 1 if EBX != 0
            assembly_code.append(f"AND AL, BL")    # AL = AL AND BL
            assembly_code.append(f"MOVZX EBX, AL") # Zero-extend AL into EBX
        elif self.value == "OR":
            assembly_code.append(f"CMP EAX, 0")    # Check if EAX is not zero
            assembly_code.append(f"SETNE AL")      # AL = 1 if EAX != 0
            assembly_code.append(f"CMP EBX, 0")    # Check if EBX is not zero
            assembly_code.append(f"SETNE BL")      # BL = 1 if EBX != 0
            assembly_code.append(f"OR AL, BL")     # AL = AL OR BL
            assembly_code.append(f"MOVZX EBX, AL") # Zero-extend AL into EBX
        else:
            raise ValueError(f"Invalid operator '{self.value}'.")
        # Do not overwrite EBX here for comparison and logical operations

        # No need to move EAX to EBX here for comparison/logical operations
        return None, 'int'



class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self,assembly_code,symbol_table,label_generator):
        #Retorna o valor do nó
        assembly_code.append(f"MOV EBX, {self.value}")
        return self.value, 'int'
    

class Identifier(Node):
    def __init__(self, value):
        super().__init__(value)

    def Evaluate(self, assembly_code,symbol_table,label_generator):
        # Get the variable's offset from the symbol table
        offset, var_type = symbol_table.get(self.value)[1]
        #Retorna o valor da variável
        assembly_code.append(f"MOV EBX, [EBP-{offset}]")
        return symbol_table.get(self.value)

class Assign(Node):
    def __init__(self, identifier, expression):
        super().__init__()
        self.children = [identifier, expression]

    def Evaluate(self, assembly_code, symbol_table,label_generator):
        var_name = self.children[0].value
        # Check if the variable is declared
        if var_name not in symbol_table.symbols:
            raise ValueError(f"Variable '{var_name}' not declared.")
        
        # Get the variable's offset from the symbol table
        offset, var_type = symbol_table.get(var_name)[1]
        # Evaluate the expression
        value, value_type = self.children[1].Evaluate(assembly_code, symbol_table,label_generator)
        
        assembly_code.append(f'MOV [EBP-{offset}], EBX')
        return None, None


class Declaration(Node):
    def __init__(self, var_type, declarations):
        super().__init__()
        self.var_type = var_type
        self.declarations = declarations

    def Evaluate(self, assembly_code, symbol_table,label_generator):
        # Default values for initialization
        default_values = {
            'int': 0,
            'str': ''
        }

        for var_name, expr in self.declarations:
            # Check if the variable is already declared
            if var_name in symbol_table.symbols:
                raise ValueError(f"Variable '{var_name}' already declared.")
            
            # Allocate space on the stack (4 bytes for int)
            assembly_code.append(f'PUSH DWORD {default_values[self.var_type]}')
            
            # Store the variable in the symbol table with its stack position
            # The offset from EBP for a new variable will depend on the current stack pointer
            offset = (len(symbol_table.symbols) + 1) * 4
            symbol_table.set(var_name, (offset, self.var_type))
            
            if expr is not None:
                # Evaluate the expression and store its result in the variable's stack location
                value, value_type = expr.Evaluate(assembly_code, symbol_table,label_generator)
                assembly_code.append(f'MOV DWORD [EBP-{offset}], {value}')
        return None, None



class Print(Node):
    def __init__(self, expression):
        super().__init__()
        self.children = [expression]

    def Evaluate(self, assembly_code,symbol_table,label_generator):
        value, type = self.children[0].Evaluate(assembly_code,symbol_table,label_generator)
        assembly_code.append(f"PUSH EBX")
        assembly_code.append(f"CALL print")
        assembly_code.append(f"POP EBX")
        return None, None



class Statements(Node):
    def __init__(self):
        super().__init__()
        self.children = []

    def Evaluate(self,assembly_code, symbol_table,label_generator):
        # Avalia cada nó filho
        for child in self.children:
            child.Evaluate(assembly_code,symbol_table,label_generator)
        return None, None  


class If(Node):
    def __init__(self, condition, true_block, false_block=None):
        super().__init__()
        self.children = [condition, true_block]
        if false_block:
            self.children.append(false_block)

    def Evaluate(self, assembly_code, symbol_table, label_generator):
        # Generate unique labels
        label_count = label_generator.get_label_count()
        false_label = f"ELSE_{label_count}"
        end_label = f"END_IF_{label_count}"
        
        # Evaluate the condition
        condition_value, condition_type = self.children[0].Evaluate(assembly_code, symbol_table, label_generator)
        
        # The result of the condition is assumed to be in EBX
        # Compare the condition result with 0
        assembly_code.append(f"CMP EBX, 0")
        
        if len(self.children) == 3:
            # If there's an else block
            assembly_code.append(f"JE {false_label}")  # Jump to else block if condition is false
            # True block
            self.children[1].Evaluate(assembly_code, symbol_table, label_generator)
            assembly_code.append(f"JMP {end_label}")   # Jump to end after true block
            # Else block
            assembly_code.append(f"{false_label}:")
            self.children[2].Evaluate(assembly_code, symbol_table, label_generator)
            # End label
            assembly_code.append(f"{end_label}:")
        else:
            # No else block
            assembly_code.append(f"JE {end_label}")    # Jump to end if condition is false
            # True block
            self.children[1].Evaluate(assembly_code, symbol_table, label_generator)
            # End label
            assembly_code.append(f"{end_label}:")
        
        return None, None


class While(Node):
    def __init__(self, condition, block):
        super().__init__()
        self.children = [condition, block]

    def Evaluate(self, assembly_code,symbol_table,label_generator):
        # Generate unique labels
        label_count = label_generator.get_label_count()
        loop_label = f"LOOP_{label_count}"
        end_label = f"EXIT_{label_count}"
        assembly_code.append(f"{loop_label}:")
        condition_value, condition_type = self.children[0].Evaluate(assembly_code,symbol_table,label_generator)
        assembly_code.append(f"CMP EBX, 0")
        assembly_code.append(f"JE {end_label}")
        self.children[1].Evaluate(assembly_code,symbol_table,label_generator)
        assembly_code.append(f"JMP {loop_label}")
        assembly_code.append(f"{end_label}:")
        return None, None  

