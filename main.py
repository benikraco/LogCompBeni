import sys

input_expression = " ".join(sys.argv[1:])

operation = 0
signal = 1
index = 0

# Check if the input is valid
for n in range(len(input_expression)):

    i = input_expression[n]
    
    # If the input is not a number, a plus or a minus, raise an exception
    if not i.isdigit() and i not in ['+', '-']:
        raise Exception("Invalid input: '{}'".format(input_expression[n]))

    # If the input is a plus or a minus, check if the next character is a number
    if i == '+':
        operation += int(input_expression[index:n]) * signal 
        signal = 1 
        index = n + 1 

    # If the input is a plus or a minus, check if the next character is a number
    elif i == '-':
        operation += int(input_expression[index:n]) * signal 
        signal = -1 
        index = n + 1

    # If the input is the last character, add the number to the operation
    if n == len(input_expression) - 1:
        operation += int(input_expression[index:]) * signal

print(operation)