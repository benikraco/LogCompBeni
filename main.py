import sys

# join all command line arguments with spaces
input_expression = " ".join(sys.argv[1:])

# define the Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

# define the Tokenizer class
class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
    
    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position] == ' ':
            self.position += 1
        if self.position < len(self.source):
            if self.source[self.position] == "+":
                self.next = Token("PLUS", self.source[self.position])
                self.position += 1
                return self.next
            elif self.source[self.position] == "-":
                self.next = Token("MINUS", self.source[self.position])
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

# define the Parser class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
    
    @staticmethod
    def parseExpression(tokens):
        tokens.selectNext()
        result = 0

        while tokens.next.type == "SPACE":
            tokens.selectNext()

        if tokens.next.type == "ERROR":
            raise Exception("Invalid")
        
        if tokens.next.type == "INT":
            result = int(tokens.next.value)
            tokens.selectNext()
            while tokens.next.type == "PLUS" or tokens.next.type == "MINUS":
                if tokens.next.type == "PLUS":
                    tokens.selectNext()
                    while tokens.next.type == "SPACE":
                        tokens.selectNext()
                    if tokens.next.type == "INT":
                        result += int(tokens.next.value)
                        tokens.selectNext()
                    else:
                        raise Exception("Invalid")

                elif tokens.next.type == "MINUS":
                    tokens.selectNext()
                    while tokens.next.type == "SPACE":
                        tokens.selectNext()
                    if tokens.next.type == "INT":
                        result -= int(tokens.next.value)
                        tokens.selectNext()
                    else:
                        raise Exception("Invalid")

            if tokens.next.type == "EOF":
                return result
            
        else:
            raise Exception("Invalid")
    
    @staticmethod
    def run(code):
        tokens = Tokenizer(code)
        parsed = Parser.parseExpression(tokens)

        if parsed is not None:
            return parsed

# define the main function
def main():
    try:
        result = Parser.run(input_expression)
        print(result)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
