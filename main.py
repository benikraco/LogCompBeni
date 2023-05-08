import sys
import re

# Define main python reserved words
reserved_words = ["println", "if", "end", "else", "while", "readline", 'Int', 'String']


# define the Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

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
            return

        elif self.source[self.position].isdigit():
            token = self.source[self.position]
            i = 1
            while token.isdigit():
                i += 1
                if self.position + i > len(self.source):
                    break
                token = self.source[self.position : self.position + i]

            self.next = Token('Int', int(self.source[self.position : self.position + i - 1]))
            self.position += i - 1
            return

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

        elif self.source[self.position] == ":":
            self.position += 1
            if self.source[self.position] == ":":
                self.next = Token("TYPE_ANNOT", "::")
                self.position += 1
            else:
                sys.stderr.write('[ERRO] Erro léxico: : não é um token válido\n')
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
                sys.stderr.write('[ERRO] Erro léxico: string não fechada\n')
                sys.exit()

            self.next = Token('String', self.source[self.position + 1 : self.position + i])
            self.position += i + 1

        elif self.source[self.position].isalnum() or self.source[self.position] == "_":

            token = self.source[self.position]
            i = 1
            while self.position + i < len(self.source) and (self.source[self.position + i].isalnum() or self.source[self.position + i] == "_"):
                i += 1
                token = self.source[self.position : self.position + i]

            self.next = Token("ID", token)
            self.position += i

            if self.next.value in reserved_words:
                if self.next.value == "println":
                    self.next = Token("PRINTLN", self.next.value)
        
                elif self.next.value == "if":
                    self.next = Token("IF", self.next.value)
                
                elif self.next.value == "else":
                    self.next = Token("ELSE", self.next.value)
                
                elif self.next.value == "while":
                    self.next = Token("WHILE", self.next.value)

                elif self.next.value == "end":
                    self.next = Token("END", self.next.value)
            
                elif self.next.value == "readline":
                    self.next = Token("READLINE", self.next.value)
                
                elif self.next.value == 'Int':
                    self.next = Token("TYPE", self.next.value)

                elif self.next.value == 'String':
                    self.next = Token("TYPE", self.next.value)

        else:
            sys.stderr.write('[ERROR - SelectNext] Invalid token\n')
            sys.exit()

class Node:
    def __init__(self, value: str, children: list = None):
        self.value = value
        self.children = children if children is not None else []

    def evaluate(self):
        pass
        
class BinOp(Node):

    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):

        left_value, left_type = self.children[0].evaluate()
        right_value, right_type = self.children[1].evaluate()

        if left_type == 'Int' and right_type == 'Int':
            if self.value == '+':
                return (left_value + right_value, 'Int')
            elif self.value == '-':
                return (left_value - right_value, 'Int')
            elif self.value == '*':
                return (left_value * right_value, 'Int')
            elif self.value == '/':
                return (left_value // right_value, 'Int')
            elif self.value == '==':
                return (int(left_value == right_value), 'Int')
            elif self.value == '<':
                return (int(left_value < right_value), 'Int')
            elif self.value == '>':
                return (int(left_value > right_value), 'Int')
            elif self.value == '&&':
                return (int(left_value and right_value), 'Int')
            elif self.value == '||':
                return (int(left_value or right_value), 'Int')
            elif self.value == '.':
                return (str(left_value) + str(right_value), 'String')
            else:
                sys.stderr.write('[ERROR] Invalid operator\n')
                sys.exit()
        
        elif left_type == 'String' and right_type == 'String':
            if self.value == '.':
                return (str(left_value) + str(right_value), 'String')
            elif self.value == '==':
                res = str(left_value) == str(right_value)
                return (int(res), 'Int')
            elif self.value == '<':
                res = str(left_value) < str(right_value)
                return (int(res), 'Int')
            elif self.value == '>':
                res = str(left_value) > str(right_value)
                return (int(res), 'Int')
            else:
                sys.stderr.write('[ERROR] Invalid operator\n')
                sys.exit()
        
        else:
            if self.value == '==':
                result = str(left_value) == str(right_value)
                return (int(result), 'Int')
    
            elif self.value == '.':
                result = str(left_value) + str(right_value)
                return (str(result), 'String')

            else:
                sys.stderr.write('[ERROR] Invalid operator\n')
                sys.exit()


class UnOp(Node):

    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):

        value, type = self.children[0].evaluate()

        if type == 'Int':
            if self.value == '+':
                return (value, 'Int')
            elif self.value == '-':
                return (-value, 'Int')
            elif self.value == '!':
                return ((not value), 'Int')
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
        return (int(self.value), 'Int')
    
class NoOp(Node):

    def __init__ (self, children = []):
        super().__init__(None, children)
        
    def evaluate(self):
        return 0

class SymbolTable():
    
    tab = {}

    @staticmethod
    def creator(key, value, type):
        if key not in SymbolTable.tab.keys():
            SymbolTable.tab[key] = (value, type)
        else:
            sys.stderr.write('[ERROR] Variable already declared\n')
            sys.exit()

    @staticmethod
    def setter(key, value, type):
        if key not in SymbolTable.tab.keys():
            sys.stderr.write('[ERROR] Variable not declared\n')
            sys.exit()
        
        elif type == SymbolTable.tab[key][1]:
            SymbolTable.tab[key] = (value, type)

        else:
            sys.stderr.write('[ERROR] Variable type mismatch\n')
            sys.exit()

    @staticmethod
    def getter(key):
        if key in SymbolTable.tab.keys():
            return SymbolTable.tab[key]
        else:
            sys.stderr.write('[ERROR] Variable not declared\n')
            sys.exit()
    
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
        value = self.children[0].evaluate()[0]
        print(value)
        return value

class Readline(Node):
    def __init__ (self):
        pass

    def evaluate(self):
        return (int(input()), 'Int')

class If(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        if self.children[0].evaluate()[0]:
            self.children[1].evaluate()
        elif len(self.children) > 2:
            self.children[2].evaluate()

class While(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        while self.children[0].evaluate()[0]:
            self.children[1].evaluate()
            

class Assign(Node):
    def __init__ (self, value,  children = []):
        super().__init__(value, children)

    def evaluate(self):
        value, type = self.children[1].evaluate()
        SymbolTable.setter(self.children[0].value, value, type)

class Block(Node):
    def __init__ (self, value, children = []):
        super().__init__(value, children)

    def evaluate(self):
        for child in self.children:
            child.evaluate()

class VarDec(Node):
    def __init__ (self, value, children = []):
        super().__init__(value, children)

    def evaluate(self):
        id = self.children[0].value
        value = self.children[1]

        if isinstance(value, Node):
            value = value.evaluate()[0]
        
        SymbolTable.creator(id, value, self.value)

class StringVal(Node):
    def __init__ (self, value, children = []):
        super().__init__(value, children)

    def evaluate(self):
        return (str(self.value), 'String')
    

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
             
        # verify if it's multiplication or division
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
        if tokens.next.type == 'Int':
            value = tokens.next.value
            result = IntVal(value, [])
            tokens.selectNext()
            return result
        
        #verify if the next token is a string
        elif tokens.next.type == 'String':
            value = tokens.next.value
            result = StringVal(value, [])
            tokens.selectNext()
            return result

        # verify if the next token is an identifier
        elif tokens.next.type == "ID":
            result = Identifier(tokens.next.value, [])
            tokens.selectNext()
            return result
        
        # verify if it's plus or minus
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
        
        # verify identifier
        elif tokens.next.type == "ID":
            result = tokens.next.value
            tokens.selectNext()
            return Identifier(result, [])
        
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

    def ParseStatement(tokens):

        # verify identifier
        if tokens.next.type == "ID":
            id = Identifier(tokens.next.value, [])
            tokens.selectNext()

            if tokens.next.type == "ASSIGN":
                tokens.selectNext()
                res = Assign("=", [id, Parser.ParseExpression(tokens)])

            elif tokens.next.type == "TYPE_ANNOT":
                tokens.selectNext()
                
                if tokens.next.type == "TYPE":
                    value_type = tokens.next.value
                    tokens.selectNext()

                    if tokens.next.type == "ASSIGN":
                        tokens.selectNext()
                        res = VarDec(value_type, [id, Parser.ParseRelExpression(tokens)])
                    else:
                        if value_type == 'Int':
                            value = 0
                        elif value_type == 'String':
                            value = ""
                        res = VarDec(value_type, [id, value])
                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing type")
                    sys.exit()

            if tokens.next.type == "NEWLINE":
                return res
            else: 
                sys.stderr.write("[ERROR - ParseStatement] - Missing newline - 1")
                sys.exit()
        
        # verify print
        elif tokens.next.type == "PRINTLN":
            tokens.selectNext()

            # verify open parenthesis
            if tokens.next.type == "PAR_OPEN":
                tokens.selectNext()
                res = Println("PRINTLN", [Parser.ParseRelExpression(tokens)])

                # verify close parenthesis
                if tokens.next.type == "PAR_CLOSE":
                    tokens.selectNext()
                    if tokens.next.type == "NEWLINE":
                        return res
                    else:
                        sys.stderr.write("[ERROR - ParseStatement] - Missing newline - 2")
                        sys.exit()

                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing close parenthesis")
                    sys.exit()

        # verify while
        elif tokens.next.type == "WHILE":
            tokens.selectNext()
            var = Parser.ParseRelExpression(tokens)
            while_child = []

            # verify new line
            if tokens.next.type == "NEWLINE":
                tokens.selectNext()
    
                
                # verify end
                while tokens.next.type != "END":
                    while_child.append(Parser.ParseStatement(tokens))
                    tokens.selectNext()

                while_block = Block(while_child)

                if tokens.next.type == "END":
                    tokens.selectNext()
                    return While("WHILE", [var, while_block])
                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing end")
                    sys.exit()

            else:
                sys.stderr.write("[ERROR - ParseStatement] - Missing newline - 3")
                sys.exit()
                
        elif tokens.next.type == "IF":
            tokens.selectNext()
            var = Parser.ParseRelExpression(tokens)

            if tokens.next.type == "NEWLINE":
                tokens.selectNext()
                if_child = []

                while tokens.next.type != "END" and tokens.next.type != "ELSE":
                    if_child.append(Parser.ParseStatement(tokens))
                    tokens.selectNext()

                if_block = Block(if_child)

                if tokens.next.type == "ELSE":
                    tokens.selectNext()

                    if tokens.next.type == "NEWLINE":

                        tokens.selectNext()
                        else_child = []

                        while tokens.next.value != "END":
                            else_child.append(Parser.ParseStatement(tokens))
                            tokens.selectNext()
                        
                        else_block = Block(else_child)

                        if tokens.next.type == "END":
                            tokens.selectNext()
                            return If("IF", [var, if_block, else_block])
                        
                        else:
                            sys.stderr.write("[ERROR - ParseStatement] - Missing end")
                            sys.exit()

                elif tokens.next.type == "END":
                    tokens.selectNext()
                    return If("IF", [var, if_block])
                
                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing end")
                    sys.exit()
            
            else:
                sys.stderr.write("[ERROR - ParseStatement] - Missing newline - 4")
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

    # Pre-process the input file
    result = PrePro.filter(arq)
    res = Parser.run(result)
    print(res)  


if __name__ == "__main__":
    main()

