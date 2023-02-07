import sys

input_expression = " ".join(sys.argv[1:])

operation = 0
signal = 1
index = 0

for n in range(len(input_expression)):
    i = input_expression[n]
    
    if not i.isdigit():
        if i == '+':
            operation += int(input_expression[index:n]) * signal
            signal = 1
            index = n + 1
        elif i == '-':
            operation += int(input_expression[index:n]) * signal
            signal = -1
            index = n + 1
    if n == len(input_expression) - 1:
        operation += int(input_expression[index:]) * signal

print(operation)