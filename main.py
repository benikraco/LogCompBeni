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
    def __init__(self, value, children = []):
        self.value = value
        self.children = children

    def evaluate(self):
        pass
        
class BinOp(Node):

    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        left_value, left_type = self.children[0].evaluate()
        right_value, right_type = self.children[1].evaluate()

    
        if left_type == "Int" and right_type == "Int":
            if self.value == '+':
                return (left_value + right_value, "Int")
            elif self.value == '-':
                return (left_value - right_value, "Int")
            elif self.value == '*':
                return (left_value * right_value, "Int")
            elif self.value == '/':
                return (int(left_value // right_value), "Int")
            elif self.value == '==':
                return (int(left_value == right_value, "Int"))
            elif self.value == '>':
                return (int(left_value > right_value, "Int"))
            elif self.value == '<':
                return (int(left_value < right_value, "Int"))
            elif self.value == '&&':
                return (left_value and right_value, "Int")
            elif self.value == '||':
                return (left_value or right_value, "Int")
            elif self.value == '.':
                return (str(left_value) + str(right_value), "String")
            else:
                sys.stderr.write('[ERROR] Invalid operator\n')
                sys.exit()
            
        elif left_type == "String" and right_type == "String":
            if self.value == '.':
                return (left_value + right_value, "String")
            elif self.value == '==':
                return (int(left_value == right_value, "String"))
            elif self.value == '>':
                res = str(left_value) > str(right_value)
                return (int(res), "Int")
            elif self.value == '<':
                res = str(left_value) < str(right_value)
                return (int(res), "Int")
            else:
                sys.stderr.write('[ERROR] Invalid operator\n')
                sys.exit()
        
        else:
            if self.value == ".":
                res = str(left_value) + str(right_value)
                return (str(res), "String")
            elif self.value == "==":
                res = str(left_value) == str(right_value)
                return (int(res), "Int")
            else:
                sys.stderr.write('[ERROR] Invalid operator\n')
                sys.exit()


class UnOp(Node):

    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        value, type = self.children[0].Evaluate()

        if type == 'Int':
            if self.value == '-':
                return (-value, 'Int')
            elif self.value == '!':
                return (not value, 'Int')
            else:
                return (value, 'Int')
        else:
            sys.stderr.write('[ERRO] Operador inválido.\n')
            sys.exit()
        
class IntVal(Node):

    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        return (int(self.value), "Int")
    
class StringVal(Node):
    
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        return (str(self.value), "String")
    
class VarDec(Node):
    
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        id = self.children[0]
        value = self.children[1]

        if isinstance(value, Node):
            value = value.evaluate()[0]

        SymbolTable.creator(id.value, value, self.value)
class NoOp(Node):

    def __init__ (self, children = []):
        super().__init__(None, children)
        
    def evaluate(self):
        return None

class SymbolTable():
    table = {}

    @staticmethod
    def creator(key, value, type):
        if key in SymbolTable.table.keys():
            sys.stderr.write('[ERRO] A variável já foi declarada.\n')
            sys.exit()
        else:
            SymbolTable.table[key] = (value, type)
    
    @staticmethod
    def getter(key):
        if key in SymbolTable.table.keys():
            return SymbolTable.table[key]
        else:
            sys.stderr.write('[ERRO] A variável não foi declarada.\n')
            sys.exit()
    
    @staticmethod
    def setter(key, value, type):
        if key not in SymbolTable.table.keys():
            sys.stderr.write('[ERRO] A variável não foi declarada.\n')
            sys.exit()
        elif type != SymbolTable.table[key][1]:
            sys.stderr.write('[ERRO] A variável não é do tipo correto.\n')
            sys.exit()
        
        SymbolTable.table[key] = (value, type)
    
class Identifier(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)


    def evaluate(self):
        var = SymbolTable.getter(self.value)
        return (var[0], var[1])

class Println(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        res = self.children[0].evaluate()
        if res is not None:
            print(res)

class Readline(Node):
    def __init__ (self):
        pass

    def evaluate(self):
        return (int(input()), "Int")

class If(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        if self.children[0].evaluate():
            self.children[1].evaluate()
        elif len(self.children) > 2:
            self.children[2].evaluate()

class While(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        while self.children[0].evaluate():
            self.children[1].evaluate()

class Assign(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        SymbolTable.setter(self.children[0].value, self.children[1].evaluate())

class Block(Node):
    def __init__ (self, value, children = []):
        super().__init__(value, children)

    def evaluate(self):
        for child in self.children:
            child.evaluate()


# define the Tokenizer class
class Tokenizer:
    def __init__(self, source, next):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):

        while self.position < len(self.source) and self.source[self.position] in (" ", "\t"):
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return self.next

        if self.source[self.position].isdigit():
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isdigit():
                self.position += 1
            self.next = Token("INT", int(self.source[start:self.position]))

        elif self.source[self.position].isalpha() or self.source[self.position] == "_":
            token = self.source[self.position]
            i = 1
            while self.position + i < len(self.source) and (self.source[self.position + i].isalnum() or self.source[self.position + i] == "_"):
                i += 1
                token = self.source[self.position:self.position + i]
            
            self.next = Token("ID", token)
            self.position += i

            if self.next.value in reserved_words:
                if self.next.value == "if":
                    self.next = Token("IF", self.next.value)
                elif self.next.value == "println":
                       self.next = Token("PRINTLN", self.next.value)
                elif self.next.value == "else":
                    self.next = Token("ELSE", self.next.value)
                elif self.next.value == "while":
                    self.next = Token("END", self.next.value)
                elif self.next.value == "end":
                    self.next = Token("NEWLINE", self.next.value)
                elif self.next.value == "readline":
                    self.next = Token("READLINE", self.next.value)
                elif self.next.value == "Int":
                    self.next = Token("TYPE", self.next.value)
                elif self.next.value == "String":
                    self.next = Token("TYPE", self.next.value)
                
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
            if self.source[self.position + 1] == "=":
                self.next = Token("EQUAL", "==")
                self.position += 2
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
                sys.stderr.write(f'[ERROR - SelectNext] Invalid token\n {self.source[self.position]}')
                sys.exit()
        
        elif self.source[self.position] == "|":
            self.position += 1
            if self.source[self.position] == "|":
                self.next = Token("OR", "||")
                self.position += 1
            else:
                sys.stderr.write(f'[ERROR - SelectNext] Invalid token\n {self.source[self.position]}')
                sys.exit()

        elif self.source[self.position] == "!":
            self.next = Token("NOT", "!")
            self.position += 1
        
        elif self.source[self.position] == "\n":
            self.next = Token("NEWLINE", "\n")
            self.position += 1
        
        elif self.source[self.position] == ":":
            self.position += 1
            if self.source[self.position] == ":":
                self.next = Token("TYPE_ANNOT", "::")
                self.position += 1
            else:
                sys.stderr.write(f'[ERROR - SelectNext] Invalid token\n {self.source[self.position]}')
                sys.exit()

        elif self.source[self.position] == ".":
            self.next = Token("CONCAT", ".")
            self.position += 1

        elif self.source[self.position] == "\"":
            token = self.source[self.position]
            i = 1
            while self.position + i < len(self.source) and self.source[self.position + i] != "\"":
                i += 1
                token = self.source[self.position : self.position + i]

            if self.position + i >= len(self.source):
                sys.stderr.write('[ERROR - SelectNext] String not closed\n')
                sys.exit()

            self.next = Token("STRING", self.source[self.position + 1 : self.position + i])
            self.position += i + 1

        else:
            sys.stderr.write(f'[ERROR - SelectNext] Invalid token\n {self.source[self.position]}')
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
             
        # verify if it's multiplication or division or and
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

        #verify if the next token is an integer
        if tokens.next.type == "INT":
            value = tokens.next.value
            result = IntVal(value, [])
            tokens.selectNext()
            return result

        elif tokens.next.type == "STRING":
            value = tokens.next.value
            result = StringVal(value, [])
            tokens.selectNext()
            return result
        
        # verify identifier
        elif tokens.next.type == "ID":
            result = tokens.next.value
            tokens.selectNext()
            return Identifier(result, [])
        
        # verify if it's plus or minus or not
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
        elif tokens.next.type == "READLINE":
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

    @staticmethod
    def ParseStatement(tokens):

        # verify identifier
        if tokens.next.type == "ID":
            ident = Identifier(tokens.next.type, [])
            tokens.selectNext()

            if tokens.next.type == "ASSIGN":
                tokens.selectNext()
                var = Parser.ParseRelExpression(tokens)
                result = Assign("=", [ident, var])

            elif tokens.next.type == "TYPE_ANNOT":
                tokens.selectNext()

                if tokens.next.type == "TYPE":
                    var_type = tokens.next.value
                    tokens.selectNext()

                    if tokens.next.type == "ASSIGN":
                        tokens.selectNext()
                        var = Parser.ParseRelExpression(tokens)
                        result = VarDec(var_type, [ident, var])

                    else:
                        if var_type == "Int":
                            val = 0
                        elif var_type == "String":
                            val = ""
                        result = VarDec(var_type, [ident, val])
                        
                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing type")
                    sys.exit()
            else:
                sys.stderr.write("[ERROR - ParseStatement] - Missing assignment")
                sys.exit()

            if tokens.next.type == "NEWLINE":
                return result
            else:
                sys.stderr.write("[ERROR - ParseStatement] - Missing end")
                sys.exit()

        
        # verify print
        if tokens.next.type == "PRINTLN":
            tokens.selectNext()

            # verify open parenthesis
            if tokens.next.type == "PAR_OPEN":
                tokens.selectNext()
                result = Println("PRINTLN", [Parser.ParseRelExpression(tokens)])

                # verify close parenthesis
                if tokens.next.type == "PAR_CLOSE":
                    tokens.selectNext()
                    if tokens.next.type == "NEWLINE":
                        return result

                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing close parenthesis")
                    sys.exit()

            else:
                sys.stderr.write("[ERROR - ParseStatement] - Missing open parenthesis")
                sys.exit()

        # verify while
        elif tokens.next.type == "WHILE":
            tokens.selectNext()
            var = Parser.ParseRelExpression(tokens)

            children = []

            # verify new line
            if tokens.next.type == "NEWLINE":
                tokens.selectNext()


                # verify end
                while tokens.next.type != "END":
                    children.append(Parser.ParseStatement(tokens))
                    tokens.selectNext()

                while_blo = Block(children)

                if tokens.next.type == "END":
                    tokens.selectNext()
                    return While("WHILE", [var, while_blo])
                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing end")
                    sys.exit()

            else:
                sys.stderr.write("[ERROR - ParseStatement] - Missing new line")
                sys.exit()

        # verify if        
        elif tokens.next.type == "IF":
            tokens.selectNext()
            var = Parser.ParseRelExpression(tokens)

            if tokens.next.type == "NEWLINE":
                children_if = []
                tokens.selectNext()
                

                while tokens.next.type != "END" and tokens.next.type != "ELSE":
                    children_if.append(Parser.ParseStatement(tokens))
                    tokens.selectNext()

                block_if = Block(children_if)

                if tokens.next.type == "ELSE":
                    tokens.selectNext()

                    if tokens.next.type == "NEWLINE":
                        children_else = []
                        tokens.selectNext()

                        while tokens.next.type != "END":
                            children_else.append(Parser.ParseStatement(tokens))
                            tokens.selectNext()
                        block_else = Block(children_else)

                        if tokens.next.type == "END":
                            tokens.selectNext()
                            return If("IF", [var, block_if, block_else])
                        
                        else:
                            sys.stderr.write("[ERROR - ParseStatement] - Missing end")
                            sys.exit()

                elif tokens.next.type == "END":
                    tokens.selectNext()
                    return If("IF", [var, block_if])
                
                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing end")
                    sys.exit()
            
            else:
                sys.stderr.write("[ERROR - ParseStatement] - Missing new line")
                sys.exit()

        # verify newline
        elif tokens.next.type == "NEWLINE":
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
        nodes = []

        while tokens.next.type != "EOF":
            nodes.append(Parser.ParseStatement(tokens))
            tokens.selectNext()
        
        tokens.selectNext()
        return Block(nodes)

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
    parser = Parser(result)
    parser.run(result)

if __name__ == "__main__":
    main()
