import sys
import re

# Define main python reserved words
reserved_words = ["println", "if", "end", "else", "while", "readline", "Int", "String", "return", "function"]


# define the Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Node:
    def __init__(self, value, children = []):
        self.value = value
        self.children = children

    def evaluate(self):
        pass


class BinOp(Node):

    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self, TAB):
        l_value, l_type = self.children[0].evaluate(TAB)
        r_value, r_type = self.children[1].evaluate(TAB)


        if l_type == "String" and r_type == "String":
            if self.value == ".":
                return (str(l_value) + str(r_value), "String")
            elif self.value == "==":
                 return (int(l_value == r_value), "Int")
            elif self.value == ">":
                return (int(str(l_value) > str(r_value)), "Int")
            elif self.value == "<":
                return (int(str(l_value) < str(r_value)), "Int")
            

        elif l_type == "Int" and r_type == "Int":
            if self.value == "+":
                return (l_value + r_value, "Int")
            elif self.value == "-":
                return (l_value - r_value, "Int")
            elif self.value == "*":
                return (l_value * r_value, "Int")
            elif self.value == "/":
                return (l_value // r_value, "Int")
            elif self.value == "==":
                return (int(l_value == r_value), "Int")
            elif self.value == ">":
                return (int(l_value > r_value), "Int")
            elif self.value == "<":
                return (int(l_value < r_value), "Int")
            elif self.value == "&&":
                return (int(l_value and r_value), "Int")
            elif self.value == "||":
                return (int(l_value or r_value), "Int")
            elif self.value == ".":
                return (str(l_value) + str(r_value), "String")
            
            
        else:
            if self.value == "==":
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

    def evaluate(self, TAB):

        value_type = self.children[0].evaluate(TAB)

        if value_type[1] == "Int":
            if self.value == "+":
                return (value_type[0], "Int")
            elif self.value == "-":
                return (-value_type[0], "Int")
            elif self.value == "!":
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

    def evaluate(self, TAB):
        return (int(self.value), "Int")


class NoOp(Node):

    def __init__ (self, children = []):
        super().__init__(None, children)
        
    def evaluate(self, TAB):
        return (None)


class SymbolTable(): 
    
    tab = {}

    def creator(self, key, value, type):
        if key not in SymbolTable.tab.keys():
            SymbolTable.tab[key] = (value, type)
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
        
        SymbolTable.tab[key] = (value, type)
            
        
class Identifier(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self, TAB):
        value, type = TAB.getter(self.value)
        return (value, type)


class Println(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self, TAB):
        res = self.children[0].evaluate(TAB)[0]
        if res is not None:
            print(res)


class Readline(Node):
    def __init__ (self):
        pass

    def evaluate(self, TAB):
        return (int(input()), "Int")


class If(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self, TAB):
        if self.children[0].evaluate(TAB)[0]:
            self.children[1].evaluate(TAB)
        elif len(self.children) > 2:
            self.children[2].evaluate(TAB)


class While(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self, TAB):
        while self.children[0].evaluate(TAB)[0]:
            self.children[1].evaluate(TAB)
            

class Assign(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self, TAB): 
        ##breakpoint()

        value, type = self.children[1].evaluate(TAB)
        TAB.setter(self.children[0].value, value, type)

class VarDec(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self, TAB):
        identifier, value = self.children

        value = value.evaluate(TAB)[0] if isinstance(value, Node) else value

        TAB.creator(identifier.value, value, self.value)

class StringVal(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self, TAB):
        return (str(self.value), "String")    


class Return(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self, TAB):
        return self.children[0].evaluate(TAB)
    
class FuncTable:
    
    table = {}

    @staticmethod
    def creator(key, value):
        FuncTable.table[key] = value

    def getter(key):
        if key in FuncTable.table.keys():
            return FuncTable.table[key]
        else:
            sys.stderr.write('[ERROR] Function not declared\n')
            sys.exit()

class FuncDec(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self, TAB):
        FuncTable.creator(self.children[0].value, self)

class FuncCall(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self, TAB):
        func = FuncTable.getter(self.value)
        table = SymbolTable()
        
        if len(self.children) != (len(func.children) - 2):
            sys.stderr.write('[ERROR] Invalid number of arguments\n')
            sys.exit()

        for i in range(len(self.children)):
            x = func.children[i+1].children[0].value
            y = self.children[i].evaluate(TAB)[0]
            z = func.children[i+1].value
            table.creator(x, y, z)

        ##breakpoint()
        return func.children[-1].evaluate(table)

class Block(Node):
    def __init__ (self, value, children = []):
        super().__init__(value, children)

    def evaluate(self, TAB):
        for child in self.children:
            if isinstance(child, Return):
                return child.evaluate(TAB)
            child.evaluate(TAB)

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

        elif self.source[self.position] == ",":
            self.next = Token("COMMA", ",")
            self.position += 1

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
            name = tokens.next.value
            res = Identifier(name, [])
            tokens.selectNext()

            if tokens.next.type == "PAR_OPEN":
                args = []
                tokens.selectNext()

                if tokens.next.type != "PAR_CLOSE":
                    args.append(Parser.ParseRelExpression(tokens))
                    while tokens.next.type == "COMMA":
                        tokens.selectNext()
                        args.append(Parser.ParseRelExpression(tokens))
                
                if tokens.next.type == "PAR_CLOSE":
                    tokens.selectNext()
                    res = FuncCall(name, args)

                else:
                    sys.stderr.write("[ERROR - ParseFactor] - Missing close parenthesis")
                    sys.exit()
                
                res = FuncCall(name, args)
            
            return res
        
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
                        res = VarDec(type, [id, Parser.ParseRelExpression(tokens)])
                    else:
                        if type == "Int":
                            val = 0
                        elif type == "String":
                            val = ""
                        res = VarDec(type, [id, val])
                    
                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing type")
                    sys.exit()
            
            elif tokens.next.type == "PAR_OPEN":
                tokens.selectNext()
                args = []

                if tokens.next.type != "PAR_CLOSE":
                    args.append(Parser.ParseRelExpression(tokens))
                    while tokens.next.type == "COMMA":
                        tokens.selectNext()
                        args.append(Parser.ParseRelExpression(tokens))
                
                if tokens.next.type == "PAR_CLOSE":
                    res = FuncCall(id.value, args)
                    tokens.selectNext()
                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing close parenthesis")
                    sys.exit()
            
            else:
                sys.stderr.write("[ERROR - ParseStatement] - Missing assign or open parenthesis")
                sys.exit()

            if tokens.next.type == "NEWLINE":
                return res
            else: 
                sys.stderr.write("[ERROR - ParseStatement] - Missing newline - 3")
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
        
        # verify function
        elif tokens.next.type == "RESERVED" and tokens.next.value == "function":
            tokens.selectNext()

            if tokens.next.type == "ID":
                name = Identifier(tokens.next.value)
                tokens.selectNext()

                if tokens.next.type == "PAR_OPEN":
                    tokens.selectNext()
                    args = []

                    if tokens.next.type == "ID":
                        id = Identifier(tokens.next.value)
                        tokens.selectNext()
                        if tokens.next.type == "TYPE_ASSIGN":
                            tokens.selectNext()
                            if tokens.next.type == "TYPE":
                                type = tokens.next.value
                                args.append(VarDec(type, [id, None]))
                                tokens.selectNext()

                                while tokens.next.type == "COMMA":
                                    tokens.selectNext()
                                    if tokens.next.type == "ID":
                                        id = Identifier(tokens.next.value)
                                        tokens.selectNext()
                                        if tokens.next.type == "TYPE_ASSIGN":
                                            tokens.selectNext()
                                            if tokens.next.type == "TYPE":
                                                args.append(VarDec(tokens.next.value, [id, None]))
                                                tokens.selectNext()
                                            else:
                                                sys.stderr.write("[ERROR - ParseStatement] - Missing type")
                                                sys.exit()
                                        else:
                                            sys.stderr.write("[ERROR - ParseStatement] - Missing type assign")
                                            sys.exit()
                                    else:
                                        sys.stderr.write("[ERROR - ParseStatement] - Missing id")
                                        sys.exit()
                    
                    if tokens.next.type == "PAR_CLOSE":
                        tokens.selectNext()
                        if tokens.next.type == "TYPE_ASSIGN":
                            tokens.selectNext()
                            if tokens.next.type == "TYPE":
                                type = tokens.next.value
                                tokens.selectNext()

                                if tokens.next.type == "NEWLINE":
                                    tokens.selectNext()
                                    instru = []

                                    while tokens.next.value != "end":
                                        instru.append(Parser.ParseStatement(tokens))
                                    
                                    tokens.selectNext()
                                    lista = [name] + args + [Block("BLOCK",instru)]
                                    return FuncDec(type, lista)
                                
                                else:
                                    sys.stderr.write("[ERROR - ParseStatement] - Missing newline - 1")
                                    sys.exit()

                            else:
                                sys.stderr.write("[ERROR - ParseStatement] - Missing type")
                                sys.exit()
                        
                        else:
                            sys.stderr.write("[ERROR - ParseStatement] - Missing type assign")
                            sys.exit()
            
            else:
                sys.stderr.write("[ERROR - ParseStatement] - Missing id")
                sys.exit()
        
        # verify return
        elif tokens.next.type == "RESERVED" and tokens.next.value == "return":
            tokens.selectNext()
            
            node = Return("RETURN", [Parser.ParseRelExpression(tokens)])
            

            if tokens.next.type == "NEWLINE":
                return node

            else:
                sys.stderr.write("[ERROR - ParseStatement] - Missing newline - 2")
                sys.exit()

        
        else:
            sys.stderr.write(f"[ERROR - ParseStatement] - Invalid token: {tokens.next.type}: {tokens.next.value}")
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

        TAB = SymbolTable()
        
        return parsed.evaluate(TAB)
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

if __name__ == "__main__":
    main()

