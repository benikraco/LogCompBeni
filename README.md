# Repositório de Lógica da Computação

### Status dos testes

![git status](http://3.129.230.99/svg/benikraco/LogCompBeni/)

#### Diagrama sintático

![1677527145466](image/README/1677527145466.png)

#### EBNF

```python
EXPRESSION = TERM, { ("+" | "-"), TERM };
TERM = FACTOR, { ("*" | "/"), FACTOR };
FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | number ;
```
