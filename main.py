import sys

input_expression = " ".join(sys.argv[1:])

#Create class Token
class Token():

    def __init__(self, type, value):
        self.type = type
        self.value = value

#Create class Tokenizer
class Tokenizer():

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
    
    # Reads the next token from the source code and stores it in self.next
    def selectNext(self):
        if self.position < len(self.source):
            if self.source[self.position] == "+":
                self.next = Token("PLUS", self.source[self.position])
                self.position += 1
                return self.next
            elif self.source[self.position] == "-":
                self.next = Token("MINUS", self.source[self.position])
                self.position += 1
                return self.next
            elif self.source[self.position] == " ":
                self.next = Token("SPACE", self.source[self.position])
                self.position += 1
                return self.next
            elif self.source[self.position].isdigit():
                int = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    int += self.source[self.position]
                    self.position += 1
                self.next = Token("INT", int)
                return self.next
            else:
                self.next = Token("ERROR", self.source[self.position])
                self.position += 1
                return self.next
        else:
            self.next = Token("EOF", "EOF")
            return self.next

class Parser():

    def __init__(self, tokens):
        self.tokens = tokens
    
    # Consumes tokens and analyses the expression
    @staticmethod
    def parseExpression(tokens):

        tokens.selectNext()
        result = 0

        if tokens.next.type == "SPACE":
            while(tokens.next.type == "SPACE"):
                tokens.selectNext()

        if tokens.next.type == "ERROR":
            raise Exception("Invalid")
        
        if tokens.next.type == "INT":
            result = int(tokens.next.value)
            tokens.selectNext()
            while tokens.next.type == "PLUS" or tokens.next.type == "MINUS" or tokens.next.type == "SPACE":
                if tokens.next.type == "PLUS":
                    tokens.selectNext()
                    if tokens.next.type == "SPACE":
                        result+=0
                    elif tokens.next.type == "INT":
                        result += int(tokens.next.value)
                    else:
                        raise Exception("Invalid")

                elif tokens.next.type == "MINUS":
                    tokens.selectNext()
                    if tokens.next.type == "SPACE":
                        result-=0
                    elif tokens.next.type == "INT":
                        result -= int(tokens.next.value)
                    else:
                        raise Exception("Invalid")

                tokens.selectNext()

            if tokens.next.type == "EOF":
                return result
            
        else:
            raise Exception("Invalid")

    
    @staticmethod
    def run(code):
        tokens = Tokenizer(code)
        parsed = Parser.parseExpression(tokens)

        if parsed != None:
            return parsed

#Main function
def main():
    Parser.run(input_expression)
    print(Parser.run(input_expression))

main()