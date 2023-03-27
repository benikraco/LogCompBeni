import sys
import re

# Define main python reserved words
reserved = ["println"]

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

    def evaluate(self):
        if self.value == '+':
            return self.children[0].evaluate() + self.children[1].evaluate()
        elif self.value == '-':
            return self.children[0].evaluate() - self.children[1].evaluate()
        elif self.value == '*':
            return self.children[0].evaluate() * self.children[1].evaluate()
        elif self.value == '/':
            return int(self.children[0].evaluate() // self.children[1].evaluate())
        else:
            sys.stderr.write('[ERROR] Invalid operator\n')
            sys.exit()


class UnOp(Node):

    def evaluate(self):
        if self.value == '-':
            return -self.children[0].evaluate()
        elif self.value == '+':
            return self.children[0].evaluate()
        

class IntVal(Node):

    def evaluate(self):
        return int(self.value)
    
class NoOp(Node):
    def evaluate(self):
        return None

class SymbolTable():

    tab = {}
    
    @staticmethod
    def getter(key):
        if key in SymbolTable.tab.keys():
            return SymbolTable.tab[key]
        else:
            sys.stderr.write('[ERROR] Variable not declared\n')
            sys.exit()
    
    @staticmethod
    def setter(key, value):
        SymbolTable.tab[key] = value
    
class Identifier(Node):
    def evaluate(self):
        return SymbolTable.getter(self.value)

class Println(Node):
    def evaluate(self):
        res = self.children[0].evaluate()
        if res is not None:
            print(res)

class Assign(Node):
    def evaluate(self):
        SymbolTable.setter(self.children[0].value, self.children[1].evaluate())

class Block(Node):
    def evaluate(self):
        for child in self.children:
            res = child.evaluate()
            if isinstance(child, Println) and res is not None:
                print(res)



# define the Tokenizer class
class Tokenizer:
    def __init__(self, source, next):
        self.source = source
        self.position = 0
        self.next = next

    def selectNext(self):

        while self.position < len(self.source) and self.source[self.position] == " ":
            self.position+=1

        # Verify if the string is empty
        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return self.next

        # Verify if the next token is an integer
        elif self.source[self.position].isdigit():
            tok = self.source[self.position]
            contagem = 1

            while tok.isdigit():
                contagem += 1
                if self.position + contagem > len(self.source):
                    break
                tok = self.source[self.position: self.position + contagem]
            
            self.next = Token("INT", int(self.source[self.position: self.position + contagem - 1]))
            self.position += contagem - 1
            
            return
        
        # Verify if the next token is an identifier
        elif self.source[self.position].isalnum() or self.source[self.position] == "_":
            tok = self.source[self.position]
            contagem = 1

            while self.position + contagem < len(self.source) and (self.source[self.position + contagem].isalnum() or self.source[self.position + contagem] == "_"):
                contagem += 1
                tok = self.source[self.position: self.position + contagem]

            self.next = Token("ID", tok)
            self.position += contagem

        elif self.next.value in reserved:
            if self.next.value == "println":
                self.next = Token("PRINTLN", self.next.value)
    
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
            self.next = Token("ASSIGN", "=")
            self.position += 1
        
        elif self.source[self.position] == "\n":
            self.next = Token("NEWLINE", "\n")
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
        while tokens.next.type == "PLUS" or tokens.next.type == "MINUS":
            if tokens.next.type == "PLUS":
                tokens.selectNext()
                result = BinOp('+', [result, Parser.ParseTerm(tokens)])
            elif tokens.next.type == "MINUS":
                tokens.selectNext()
                result = BinOp('-', [result, Parser.ParseTerm(tokens)])
        
        return result

    @staticmethod
    # parse multiplication and division
    def ParseTerm(tokens):

        result = Parser.ParseFactor(tokens)
             
        # verify if it's multiplication or division
        while tokens.next.type == "MULT" or tokens.next.type == "DIV":

            if tokens.next.type == "MULT":
                tokens.selectNext()
                result = BinOp('*', [result, Parser.ParseFactor(tokens)])

            elif tokens.next.type == "DIV":
                tokens.selectNext()
                result = BinOp('/', [result, Parser.ParseFactor(tokens)])

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
        
        # verify if it's plus or minus
        elif tokens.next.type == "PLUS" or tokens.next.type == "MINUS":
            if tokens.next.type == "PLUS":
                tokens.selectNext()
                res = Parser.ParseFactor(tokens)
                result = UnOp('+', [res])
                return result
            
            elif tokens.next.type == "MINUS":
                tokens.selectNext()
                res = Parser.ParseFactor(tokens)
                result = UnOp('-', [res])
                return result
        
        # verify open parenthesis
        elif tokens.next.type == "PAR_OPEN":
            tokens.selectNext()
            result = Parser.ParseExpression(tokens)
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
        
        else:
            sys.stderr.write("[ERROR - ParseFactor] - Invalid token")
            sys.exit()

    def ParseStatement(tokens):

        # verify identifier
        if tokens.next.type == "ID":
            id = Identifier(tokens.next.value, [])
            tokens.selectNext()

            if tokens.next.type != "ASSIGN":
                sys.stderr.write("[ERROR - ParseStatement] - Missing assignment")
                sys.exit()
            
            tokens.selectNext()
            res = Assign("=", [id, Parser.ParseExpression(tokens)])

            if tokens.next.type == "NEWLINE":
                return res
            else: 
                sys.stderr.write("[ERROR - ParseStatement] - Missing newline")
                sys.exit()
        
        # verify print
        elif tokens.next.type == "PRINTLN":
            tokens.selectNext()

            # verify open parenthesis
            if tokens.next.type == "PAR_OPEN":
                tokens.selectNext()
                res = Println("PRINTLN", [Parser.ParseExpression(tokens)])

                # verify close parenthesis
                if tokens.next.type == "PAR_CLOSE":
                    tokens.selectNext()
                    return res

                else:
                    sys.stderr.write("[ERROR - ParseStatement] - Missing close parenthesis")
                    sys.exit()
        
        elif tokens.next.type == "NEWLINE":
            return NoOp(None)
        
        else:
            sys.stderr.write("[ERROR - ParseStatement] - Invalid token")
            sys.exit()

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
    res = Parser.run(result)
    print(res)

if __name__ == "__main__":
    main()
