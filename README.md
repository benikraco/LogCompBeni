# Repositório de Lógica da Computação

### Status dos testes

![git status](http://3.129.230.99/svg/benikraco/LogCompBeni/)

#### Diagrama sintático

![1677527145466](image/README/1677527145466.png)

#### EBNF

```python
BLOCK = { STATEMENT };
STATEMENT = ( λ | ASSIGNMENT | PRINT), "\n" ;
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;
PRINT = "println", "(", EXPRESSION, ")" ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```
=======
# Status dos testes

![git status](http://3.129.230.99/svg/benikraco/LogCompBeni/)
