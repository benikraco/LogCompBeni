import sys
import re

# Define main python reserved words
reserved_words = ["println", "if", "end", "else", "while", "readline", "Int", "String"]


# define the Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Node:

    # 
    i = 0

    def __init__(self, value, children = []):
        self.value = value
        self.children = children

    def evaluate(self):
        pass

    def newId(self):
        Node.i += 1
        return Node.i


class BinOp(Node):

    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        self.id = self.newId()
        l_value, l_type = self.children[0].evaluate()
        Assembler.addOutput("PUSH EBX")
        r_value, r_type = self.children[1].evaluate()
        Assembler.addOutput("POP EAX")


        if l_type == "String" and r_type == "String":
            if self.value == ".":
                return (str(l_value) + str(r_value), "String")
            
            elif self.value == "==":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_je")
                return (int(l_value == r_value), "Int")
            
            elif self.value == ">":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_jg")
                return (int(str(l_value) > str(r_value)), "Int")
            
            elif self.value == "<":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_jl")
                return (int(str(l_value) < str(r_value)), "Int")
            

        elif l_type == "Int" and r_type == "Int":

            if self.value == "+":
                Assembler.addOutput("ADD EAX, EBX")
                Assembler.addOutput("MOV EBX, EAX")
                return (l_value + r_value, "Int")
            
            elif self.value == "-":
                Assembler.addOutput("SUB EAX, EBX")
                Assembler.addOutput("MOV EBX, EAX")
                return (l_value - r_value, "Int")
            
            elif self.value == "*":
                Assembler.addOutput("IMUL EBX")
                Assembler.addOutput("MOV EBX, EAX")
                return (l_value * r_value, "Int")
            
            elif self.value == "/":
                Assembler.addOutput("IDIV EBX")
                Assembler.addOutput("MOV EBX, EAX")
                return (l_value // r_value, "Int")
            
            elif self.value == "==":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_je")
                return (int(l_value == r_value), "Int")
            
            elif self.value == ">":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_jg")
                return (int(l_value > r_value), "Int")
            
            elif self.value == "<":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_jl")
                return (int(l_value < r_value), "Int")
            
            elif self.value == "&&":
                Assembler.addOutput("AND EAX, EBX")
                return (int(l_value and r_value), "Int")
            
            elif self.value == "||":
                Assembler.addOutput("OR EAX, EBX")
                return (int(l_value or r_value), "Int")
            
            elif self.value == ".":
                return (str(l_value) + str(r_value), "String")
            
            
        else:
            if self.value == "==":
                Assembler.addOutput("CMP EAX, EBX")
                Assembler.addOutput("CALL binop_je")
                result = str(l_value) == str(r_value)
                return (int(result), "Int")
            
            elif self.value == ".":
                return (str(l_value) + str(r_value), "String")
            
            else:
                sys.stderr.write('[ERROR] Invalid operator\n')
                sys.exit()


class UnOp(Node):

    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        
        self.id = self.newId()

        value_type = self.children[0].evaluate()

        if value_type[1] == "Int":

            if self.value == "+":
                Assembler.addOutput("ADD EBX, 0")
                return (value_type[0], "Int")
            
            elif self.value == "-":
                Assembler.addOutput("MOV EAX, {}".format(value_type[0]))
                Assembler.addOutput("MOV EBX, -1")
                Assembler.addOutput("IMUL EBX")
                Assembler.addOutput("MOV EBX, EAX")
                return (-value_type[0], "Int")
            
            elif self.value == "!":
                Assembler.addOutput("NEG EBX")
                return ((not value_type[0]), "Int")
            
            else:
                sys.stderr.write('[ERROR] Invalid operator\n')
                sys.exit()
        else:
            sys.stderr.write('[ERROR] Invalid operator\n')
            sys.exit()
        

class IntVal(Node):

    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        self.id = self.newId()
        Assembler.addOutput("MOV EBX, {}".format(str(self.value)))
        return (int(self.value), "Int")


class NoOp(Node):

    def __init__ (self, children = []):
        super().__init__(None, children)
        
    def evaluate(self):
        return None


class SymbolTable(): 
    tab = {}
    shift = 0

    def creator(key, value, type):
        SymbolTable.shift += 4
        if key not in SymbolTable.tab.keys():
            SymbolTable.tab[key] = (value, type, SymbolTable.shift)
        else:
            sys.stderr.write('[ERROR] Variable already declared\n')
            sys.exit()
    
    @staticmethod
    def getter(key):
        if key in SymbolTable.tab.keys():
            return SymbolTable.tab[key]
        else:
            sys.stderr.write('[ERROR] Variable not declared\n')
            sys.exit()
    
    @staticmethod
    def setter(key, value, type):
        if key not in SymbolTable.tab.keys():
            sys.stderr.write('[ERROR] Variable not declared\n')
            sys.exit()
        
        elif type != SymbolTable.tab[key][1]:
            sys.stderr.write('[ERROR] Variable type mismatch\n')
            sys.exit()
        
        SymbolTable.tab[key] = (value, type, SymbolTable.tab[key][2])
            
        
    
class Identifier(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        value = SymbolTable.getter(self.value)
        Assembler.addOutput("MOV EBX, [EBP-{}]".format(value[2]))
        return (value[0], value[1])


class Println(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        print(self.children[0].evaluate()[0])
        Assembler.addOutput("PUSH EBX")
        Assembler.addOutput("CALL print")
        Assembler.addOutput("POP EBX")



class Readline(Node):
    def __init__ (self):
        pass

    def evaluate(self):
        return (int(input()), "Int")


class If(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        self.id = self.newId()

        Assembler.addOutput("IF_{}:".format(self.id))
        Assembler.addOutput("CMP EBX, False")

        if len(self.children) > 2:
            Assembler.addOutput("JE ELSE_{}".format(self.id))
            self.children[1].evaluate()
            Assembler.addOutput("JMP EXIT_{}".format(self.id))
            Assembler.addOutput("ELSE_{}:".format(self.id))
            self.children[2].evaluate()
            Assembler.addOutput("EXIT_{}:".format(self.id))
        else:
            Assembler.addOutput("JE EXIT_{}".format(self.id))
            self.children[1].evaluate()
            Assembler.addOutput("JMP EXIT_{}:".format(self.id))
            Assembler.addOutput("EXIT_{}:".format(self.id))


class While(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        self.id = self.newId()
        Assembler.addOutput("LOOP_{}:".format(self.id))
        Assembler.addOutput("CMP EBX, False")
        Assembler.addOutput("JE EXIT_{}".format(self.id))
        self.children[1].evaluate()
        Assembler.addOutput("JMP LOOP_{}".format(self.id))
        Assembler.addOutput("EXIT_{}:".format(self.id))
            

class Assign(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        value, type = self.children[1].evaluate()
        SymbolTable.setter(self.children[0].value, value, type)
        Assembler.addOutput("MOV [EBP-{}], EBX".format(SymbolTable.getter(self.children[0].value)[2]))

class VarDec(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        identifier, value = self.children

        value = value.evaluate()[0] if isinstance(value, Node) else value

        SymbolTable.creator(identifier.value, value, self.value)
        Assembler.addOutput("PUSH DWORD 0")

class StringVal(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        return (str(self.value), "String")       


class Block(Node):
    def __init__ (self, value, children = []):
        super().__init__(value, children)

    def evaluate(self):
        for child in self.children:
            child.evaluate()

class Assembler:

    str_w = ""
    program = ""

    for i in sys.argv[1]:
        if i != ".":
            program += i
        else:
            break

    @staticmethod
    def addOutput(string):
        Assembler.str_w += string + "\n"

    @staticmethod
    def createOutput():
        
        start = """; constantes
    SYS_EXIT equ 1
    SYS_READ equ 3
    SYS_WRITE equ 4
    STDIN equ 0
    STDOUT equ 1
    True equ 1
    False equ 0

    segment .data

    segment .bss  ; variaveis
    res RESB 1

    section .text
    global _start

    print:  ; subrotina print

    PUSH EBP ; guarda o base pointer
    MOV EBP, ESP ; estabelece um novo base pointer

    MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
    XOR ESI, ESI

    print_dec: ; empilha todos os digitos
    MOV EDX, 0
    MOV EBX, 0x000A
    DIV EBX
    ADD EDX, '0'
    PUSH EDX
    INC ESI ; contador de digitos
    CMP EAX, 0
    JZ print_next ; quando acabar pula
    JMP print_dec

    print_next:
    CMP ESI, 0
    JZ print_exit ; quando acabar de imprimir
    DEC ESI

    MOV EAX, SYS_WRITE
    MOV EBX, STDOUT

    POP ECX
    MOV [res], ECX
    MOV ECX, res

    MOV EDX, 1
    INT 0x80
    JMP print_next

    print_exit:
    POP EBP
    RET

    ; subrotinas if/while
    binop_je:
    JE binop_true
    JMP binop_false

    binop_jg:
    JG binop_true
    JMP binop_false

    binop_jl:
    JL binop_true
    JMP binop_false

    binop_false:
    MOV EBX, False
    JMP binop_exit
    binop_true:
    MOV EBX, True
    binop_exit:
    RET

    _start:

    PUSH EBP ; guarda o base pointer
    MOV EBP, ESP ; estabelece um novo base pointer

    ; codigo gerado pelo compilador

    """
        finish = """; interrupcao de saida
    POP EBP
    MOV EAX, 1
    INT 0x80
    """
        with open("{}.asm".format(Assembler.program), "w") as file:
                file.write(start + Assembler.str_w + finish)  



# define the Tokenizer class
class Tokenizer:
    def __init__(self, source, next):
        self.source = source
        self.position = 0
        self.next = next

    def selectNext(self):

        while self.position < len(self.source) and self.source[self.position] in (" ", "\t"):
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return self.next
        
        # verify if it's an integer
        if self.source[self.position].isdigit():
            n = ''
            while self.position < len(self.source) and self.source[self.position].isdigit():
                n += self.source[self.position]
                self.position += 1
            self.next = Token("INT", n)

        # verify if it's a string
        elif self.source[self.position] == '"':
            self.position += 1
            string = ""
            while self.position < len(self.source) and self.source[self.position] != '"':
                string += self.source[self.position]
                self.position += 1
            self.position += 1
            self.next = Token("STRING", string)

            # verify if " is missing
            if self.position >= len(self.source):
                sys.stderr.write('[ERROR - SelectNext] Missing "')
                sys.exit()

        # verify if it's an identifier
        elif self.position  < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
            identifier = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                identifier += self.source[self.position]
                self.position += 1

            if identifier in reserved_words:
                if identifier == "Int" or identifier == "String":
                    self.next = Token("TYPE", identifier)
                else:
                    self.next = Token("RESERVED", identifier)
            else:
                self.next = Token("ID", identifier)

        elif self.source[self.position] == "+":
            self.next = Token("PLUS", "+")
            self.position += 1

        elif self.source[self.position] == "-":
            self.next = Token("MINUS", "-")
            self.position += 1

        elif self.source[self.position] == "*":
            self.next = Token("MULT", "*")
            self.position += 1

        elif self.source[self.position] == "/":
            self.next = Token("DIV", "/")
            self.position += 1

        elif self.source[self.position] == "(":
            self.next = Token("PAR_OPEN", "(")
            self.position += 1

        elif self.source[self.position] == ")":
            self.next = Token("PAR_CLOSE", ")")
            self.position += 1

        elif self.source[self.position] == "=":
            self.position += 1
            if self.source[self.position] == "=":
                self.next = Token("EQUAL", "==")
                self.position += 1
            else:  
                self.next = Token("ASSIGN", "=")
                self.position += 1
        
        elif self.source[self.position] == "<":
            self.next = Token("LESS", "<")
            self.position += 1
        
        elif self.source[self.position] == ">":
            self.next = Token("GREATER", ">")
            self.position += 1
        
        elif self.source[self.position] == "&":
            self.position += 1
            if self.source[self.position] == "&":
                self.next = Token("AND", "&&")
                self.position += 1
            else:
                sys.stderr.write('[ERROR - SelectNext] Invalid token\n')
                sys.exit()
        
        elif self.source[self.position] == "|":
            self.position += 1
            if self.source[self.position] == "|":
                self.next = Token("OR", "||")
                self.position += 1
            else:
                sys.stderr.write('[ERROR - SelectNext] Invalid token\n')
                sys.exit()

        elif self.source[self.position] == "!":
            self.next = Token("NOT", "!")
            self.position += 1
            

        elif self.source[self.position] == "\n":
            self.next = Token("NEWLINE", "\n")
            self.position += 1

        elif self.source[self.position] == ".":
            self.next = Token("CONCAT", ".")
            self.position += 1
        
        elif self.source[self.position] == ":":
            self.position += 1
            if self.source[self.position] == ":":
                self.next = Token("TYPE_ASSIGN", "::")
                self.position += 1
            else:
                sys.stderr.write('[ERROR - SelectNext] Invalid token\n')
                sys.exit()

        else:
            sys.stderr.write('[ERROR - SelectNext] Invalid token\n')
            sys.exit()

# define the Parser class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
    
    @staticmethod
    def ParseExpression(tokens):

        result = Parser.ParseTerm(tokens)

        # verify if it's plus or minus
        while tokens.next.type == "PLUS" or tokens.next.type == "MINUS" or tokens.next.type == "OR":
            if tokens.next.type == "PLUS":
                tokens.selectNext()
                result = BinOp('+', [result, Parser.ParseTerm(tokens)])
            elif tokens.next.type == "MINUS":
                tokens.selectNext()
                result = BinOp('-', [result, Parser.ParseTerm(tokens)])
            elif tokens.next.type == "OR":
                tokens.selectNext()
                result = BinOp('||', [result, Parser.ParseTerm(tokens)])
        
        return result

    @staticmethod
    # parse multiplication and division
    def ParseTerm(tokens):

        result = Parser.ParseFactor(tokens)
             
        # verify if it's multiplication or division or and or concat
        while tokens.next.type == "MULT" or tokens.next.type == "DIV" or tokens.next.type == "AND" or tokens.next.type == "CONCAT":

            if tokens.next.type == "MULT":
                tokens.selectNext()
                result = BinOp('*', [result, Parser.ParseFactor(tokens)])

            elif tokens.next.type == "DIV":
                tokens.selectNext()
                result = BinOp('/', [result, Parser.ParseFactor(tokens)])

            elif tokens.next.type == "AND":
                tokens.selectNext()
                result = BinOp('&&', [result, Parser.ParseFactor(tokens)])

            elif tokens.next.type == "CONCAT":
                tokens.selectNext()
                result = BinOp('.', [result, Parser.ParseFactor(tokens)])

            else:
                sys.stderr.write("[ERROR - ParseTerm] - Invalid token")
                sys.exit()

        return result
    
    @staticmethod
    def ParseFactor(tokens):

        # verify if its an integer
        if tokens.next.type == "INT":
            result = int(tokens.next.value)
            tokens.selectNext()
            return IntVal(result, [])
        
        # verify identifier
        elif tokens.next.type == "ID":
            result = tokens.next.value
            tokens.selectNext()
            return Identifier(result, [])
        
        # verify string
        elif tokens.next.type == "STRING":
            result = tokens.next.value
            tokens.selectNext()
            return StringVal(result, [])

        # verify if it's plus, minus or not
        elif tokens.next.type == "PLUS" or tokens.next.type == "MINUS" or tokens.next.type == "NOT":
            if tokens.next.type == "PLUS":
                tokens.selectNext()
                res = Parser.ParseFactor(tokens)
                return UnOp('+', [res])
            
            elif tokens.next.type == "MINUS":
                tokens.selectNext()
                res = Parser.ParseFactor(tokens)
                return UnOp('-', [res])

            elif tokens.next.type == "NOT":
                tokens.selectNext()
                res = Parser.ParseFactor(tokens)
                return UnOp('!', [res])
        
        # verify open parenthesis
        elif tokens.next.type == "PAR_OPEN":
            tokens.selectNext()
            result = Parser.ParseRelExpression(tokens)
            if tokens.next.type == "PAR_CLOSE":
                tokens.selectNext()
                return result
            else:
                sys.stderr.write("[ERROR - ParseFactor] - Missing close parenthesis")
                sys.exit()
        
        ## IMPLEMENTAR ULTIMA LINHA COM READLN
        elif tokens.next.type == "RESERVED" and tokens.next.value == "readline":
            tokens.selectNext()
            if tokens.next.type == "PAR_OPEN":
                tokens.selectNext()
                if tokens.next.type == "PAR_CLOSE":
                    tokens.selectNext()
                    return Readline()
                else:
                    sys.stderr.write("[ERROR - ParseFactor] - Missing close parenthesis")
                    sys.exit()
            else:
                sys.stderr.write("[ERROR - ParseFactor] - Missing open parenthesis")
                sys.exit()

        else:
            sys.stderr.write(f"[ERROR - ParseFactor] - Invalid token {tokens.next.type}")
            sys.exit()

    def ParseStatement(tokens):

        # verify identifier
        if tokens.next.type == "ID":
            id = Identifier(tokens.next.value, [])
            tokens.selectNext()

            if tokens.next.type == "ASSIGN":
                tokens.selectNext()
                return Assign("=", [id, Parser.ParseRelExpression(tokens)])

            if tokens.next.type == "TYPE_ASSIGN":
                tokens.selectNext()

                if tokens.next.type == "TYPE":
                    type = tokens.next.value
                    tokens.selectNext()

                    if tokens.next.type == "ASSIGN":
                        tokens.selectNext()
                        return VarDec(type, [id, Parser.ParseRelExpression(tokens)])
                    else:
                        if type == "Int":
                            val = 0
                        elif type == "String":
                            val = ""
                        res = VarDec(type, [id, val])
                    
                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing type")
                    sys.exit()
            
            else:
                sys.stderr.write("[ERROR - ParseStatement] - Missing type assignment")
                sys.exit()

            if tokens.next.type == "NEWLINE":
                return res
            else: 
                sys.stderr.write("[ERROR - ParseStatement] - Missing newline")
                sys.exit()
        
        # verify print
        elif tokens.next.type == "RESERVED" and tokens.next.value == "println":
            tokens.selectNext()

            # verify open parenthesis
            if tokens.next.type == "PAR_OPEN":
                tokens.selectNext()
                print_ = Parser.ParseRelExpression(tokens)

                # verify close parenthesis
                if tokens.next.type == "PAR_CLOSE":
                    tokens.selectNext()
                    return Println("PRINTLN", [print_])

                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing close parenthesis")
                    sys.exit()

        # verify while
        elif tokens.next.type == "RESERVED" and tokens.next.value == "while":
            tokens.selectNext()
            var = Parser.ParseRelExpression(tokens)

            # verify new line
            if tokens.next.type == "NEWLINE":
                tokens.selectNext()
                blo1 = Block("BLOCK", [])
                
                # verify end
                while tokens.next.value != "end":
                    blo1.children.append(Parser.ParseStatement(tokens))
                if tokens.next.type == "RESERVED" and tokens.next.value == "end":
                    tokens.selectNext()
                    return While("WHILE", [var, blo1])
                
        elif tokens.next.type == "RESERVED" and tokens.next.value == "if":
            tokens.selectNext()
            var = Parser.ParseRelExpression(tokens)
            if tokens.next.type == "NEWLINE":
                tokens.selectNext()
                blo1 = Block("BLOCK", [])
                new = False
                control = True

                while control:
                    if tokens.next.type == "NEWLINE":
                        new = True
                        tokens.selectNext()
                    if new and (tokens.next.value == "else" or tokens.next.value == "end"):
                        control = False
                    if control:
                        blo1.children.append(Parser.ParseStatement(tokens))

                if tokens.next.type == "RESERVED" and tokens.next.value == "else":
                    tokens.selectNext()
                    if tokens.next.type == "NEWLINE":
                        tokens.selectNext()
                        else_blo = Block("BLOCK", [])
                        while tokens.next.value != "end":
                            else_blo.children.append(Parser.ParseStatement(tokens))
                        if tokens.next.type == "RESERVED" and tokens.next.value == "end":
                            tokens.selectNext()
                            return If("IF", [var, blo1, else_blo])
                        else:
                            sys.stderr.write("[ERROR - ParseStatement] - Missing end")
                            sys.exit()

                elif tokens.next.type == "RESERVED" and tokens.next.value == "end":
                    tokens.selectNext()
                    return If("IF", [var, blo1])
                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing end")
                    sys.exit()

        # verify newline
        elif tokens.next.type == "NEWLINE":
            tokens.selectNext()
            return NoOp(None)    
        
        else:
            sys.stderr.write(f"[ERROR - ParseStatement] - Invalid token: {tokens.next.type}")
            sys.exit()

    @staticmethod
    def ParseRelExpression(tokens):
        result = Parser.ParseExpression(tokens)

        # verify if it's plus or minus
        while tokens.next.type == "EQUAL" or tokens.next.type == "GREATER" or tokens.next.type == "LESS":
            if tokens.next.type == "EQUAL":
                tokens.selectNext()
                result = BinOp('==', [result, Parser.ParseExpression(tokens)])
            elif tokens.next.type == "GREATER":
                tokens.selectNext()
                result = BinOp('>', [result, Parser.ParseExpression(tokens)])
            elif tokens.next.type == "LESS":
                tokens.selectNext()
                result = BinOp('<', [result, Parser.ParseExpression(tokens)])

        return result
        
    @staticmethod         
    def ParseBlock(tokens):
        result = []

        while tokens.next.type != "EOF":
            result.append(Parser.ParseStatement(tokens))
        
        return Block("BLOCK", result)

    @staticmethod
    def run(code):
        tokens = Tokenizer(code, None)
        tokens.selectNext()
        parsed = Parser.ParseBlock(tokens)


        if tokens.next.type != "EOF":
            sys.stderr.write("[ERROR - Parser.run()] - Invalid token [EOF]")
            sys.exit()
        
        return parsed.evaluate()
class PrePro():
    @staticmethod
    def filter(text):
        filter = re.sub(r'#.*', '', text)
        return filter
    
# define the main function
def main():

    # Reads the input file 
    input_expression = sys.argv[1]

    with open(input_expression, 'r') as f:
        arq = f.read()
    
    result = PrePro.filter(arq)
    res = Parser.run(result)
    Assembler.createOutput()

if __name__ == "__main__":
    main()
