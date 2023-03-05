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
        # skip spaces
        while self.position < len(self.source) and self.source[self.position] == ' ':
            self.position += 1
        
        # check if we are at the end of the input
        if self.position < len(self.source):
            if self.source[self.position] == "+":
                self.next = Token("PLUS", self.source[self.position])
                self.position += 1
                return self.next
            
            # check for minus
            elif self.source[self.position] == "-":
                self.next = Token("MINUS", self.source[self.position])
                self.position += 1
                return self.next
            
            # check for multiplication
            elif self.source[self.position] == "*":
                self.next = Token("MULT", self.source[self.position])
                self.position += 1
                return self.next

            # check for division
            elif self.source[self.position] == "/":
                self.next = Token("DIV", self.source[self.position])
                self.position += 1
                return self.next
            
            # check for space
            elif self.source[self.position].isdigit():
                int = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    int += self.source[self.position]
                    self.position += 1
                self.next = Token("INT", int)
                return self.next
            
            # check for error
            else:
                self.next = Token("ERROR", self.source[self.position])
                self.position += 1
                return self.next
        # if we are at the end of the input, return EOF    
        else:
            self.next = Token("EOF", "EOF")
            return self.next

# define the Parser class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    @staticmethod
    # parse multiplication and division
    def ParseTerm(tokens):

        # skip spaces
        tokens.selectNext()
        result = 0

        # skip spaces
        while tokens.next.type == "SPACE":
            tokens.selectNext()

        # check for error
        if tokens.next.type == "ERROR":
            sys.stderr.write('[ERRO]\n')
            sys.exit()

        # check for integer
        if tokens.next.type == "INT":
            result = int(tokens.next.value)
            tokens.selectNext()
            
            # check for multiplication or division
            while tokens.next.type == "MULT" or tokens.next.type == "DIV":

                # check for multiplication
                if tokens.next.type == "MULT":
                    tokens.selectNext()
                    while tokens.next.type == "SPACE":
                        tokens.selectNext()
                    if tokens.next.type == "INT":
                        result *= int(tokens.next.value)
                        tokens.selectNext()
                    else:
                        sys.stderr.write('[ERRO]\n')
                        sys.exit()
                
                # check for division
                elif tokens.next.type == "DIV":
                    tokens.selectNext()
                    while tokens.next.type == "SPACE":
                        tokens.selectNext()
                    if tokens.next.type == "INT":
                        result /= int(tokens.next.value)
                        tokens.selectNext()
                    else:
                        sys.stderr.write('[ERRO]\n')
                        sys.exit()

                if tokens.next.type == "EOF":
                    return result
                    
                else:
                    sys.stderr.write('[ERRO]\n')
                    sys.exit()

            return result
        
        else:
            sys.stderr.write('[ERRO]\n')
            sys.exit()
    
    @staticmethod
    def parseExpression(tokens):
        result = Parser.ParseTerm(tokens)

        while tokens.next.type == "PLUS" or tokens.next.type == "MINUS":
            if tokens.next.type == "PLUS":
                result += Parser.ParseTerm(tokens)
            elif tokens.next.type == "MINUS":
                result -= Parser.ParseTerm(tokens)
        
        tokens.selectNext()
        if tokens.next.type == "EOF":
            return result
    
    @staticmethod
    def run(code):
        tokens = Tokenizer(code)
        parsed = Parser.parseExpression(tokens)

        if parsed is not None:
            return parsed
        
class PrePro:
    @staticmethod

    # filter the input excluding comments
    def filter(text):
        comment = False
        filtered = ""

        for i in range(len(text)):
            if text[i] == "/" and text[i + 1] == "/":
                if i>2:
                    filtered = filtered[:i-2]
                else:
                    filtered = filtered[:i-1]
                comment = True
                break
            if not comment:
                filtered += text[i]
        
        return filtered


# define the main function
def main():
    result = Parser.run(PrePro.filter(input_expression))
    print(result)

if __name__ == "__main__":
    main()
