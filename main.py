import sys
import re

# join all command line arguments with spaces
input_expression = " ".join(sys.argv[1:])

# define the Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class PrePro():
    @staticmethod
    def filter(text):
        filter = re.sub(r'#.*', '', text)
        return filter

# define the Tokenizer class
class Tokenizer:
    def __init__(self, source, next):
        self.source = source
        self.position = 0
        if next == None:
            self.next = Token("INT", 0)
        else: 
            self.next = Token(self.next.type, self.next.value)
    
    def selectNext(self):
        token_incomplete=True
        num=""

        while self.position < len(self.source) and self.source[self.position] == " ":
            self.position+=1

        if self.position < len(self.source): #esse é o EOF 
            
            if self.source[self.position] == "+":
                self.next = Token("PLUS", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == "-":
                self.next = Token("MINUS", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == "*":
                self.next = Token("MULT", self.source[self.position])

                self.position += 1

                return self.next
            
            elif self.source[self.position] == "/":
                self.next = Token("DIV", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == "(":
                self.next = Token("PAR_OPEN", self.source[self.position])

                self.position += 1

                return self.next

            elif self.source[self.position] == ")":
                self.next = Token("PAR_CLOSE", self.source[self.position])

                self.position += 1

                return self.next


            else: #futuramente implementar enum pra verificar se é numero mesmo
                if self.source[self.position].isdigit():
                    num+=self.source[self.position]
                else:
                    self.next = Token("ERROR", self.source[self.position])
                    self.position+=1
                    return self.next
                
                if self.position == len(self.source)-1:
                    token_incomplete = False
                else:
                    for i in range(self.position,len(self.source)):
                        if token_incomplete:
                            if i != len(self.source) - 1:
                                if self.source[i+1].isdigit():
                                    num+=self.source[i+1]
                                else:
                                    token_incomplete = False
                            else:
                                token_incomplete = False
                    
            if token_incomplete == False:
                self.next = Token("INT", int(num))
                self.position += len(num)
                token_incomplete = True
                num = ""
                return self.next

        else:
            self.next = Token("EOF", "")
            return self.next

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
                    result += Parser.ParseTerm(tokens)
    
                elif tokens.next.type == "MINUS":
                    tokens.selectNext()
                    result -= Parser.ParseTerm(tokens)
    
                else:
                    sys.stderr.write("[ERROR]")
                    sys.exit()
            
        return result

    @staticmethod
    # parse multiplication and division
    def ParseTerm(tokens):

        result = Parser.ParseFactor(tokens)
             
        # verify if it's multiplication or division
        while tokens.next.type == "MULT" or tokens.next.type == "DIV":

            if tokens.next.type == "MULT":
                tokens.selectNext()
                result *= int(Parser.ParseFactor(tokens))

            elif tokens.next.type == "DIV":
                tokens.selectNext()
                result //= int(Parser.ParseFactor(tokens))

            else:
                sys.stderr.write("[ERROR]")
                sys.exit()

        return result
        
    def ParseFactor(tokens):

        #verify if the next token is an integer
        if tokens.next.type == "INT":
            result = tokens.next.value
            tokens.selectNext()
            return result
        
        # verify if it's plus or minus
        elif tokens.next.type == "PLUS" or tokens.next.type == "MINUS":
            if tokens.next.type == "PLUS":
                tokens.selectNext()
                return Parser.ParseFactor(tokens)
            elif tokens.next.type == "MINUS":
                tokens.selectNext()
                return -Parser.ParseFactor(tokens)
        
        # verify open parenthesis
        elif tokens.next.type == "PAR_OPEN":
            tokens.selectNext()
            result = Parser.ParseExpression(tokens)
            if tokens.next.type == "PAR_CLOSE":
                tokens.selectNext()
                return result
            else:
                sys.stderr.write("[ERROR]")
                sys.exit()
        else:
            sys.stderr.write("[ERROR]")
            sys.exit()
    
    @staticmethod
    def run(code):
        tokens = Tokenizer(code, None)
        tokens.selectNext()
        parsed = Parser.ParseExpression(tokens)

        if tokens.next.type != "EOF":
            sys.stderr.write('[ERRO]\n')
            sys.exit()

        return parsed
    
# define the main function
def main():
    result = (PrePro.filter(input_expression))
    res = Parser.run(result)
    print(res)

if __name__ == "__main__":
    main()
