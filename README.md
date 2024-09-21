# Compilador

Ebnf:

BLOCK = "{", { STATEMENT }, "}";

STATEMENT = ( λ | ASSIGNMENT | PRINTF | IF_STATEMENT | WHILE_STATEMENT | BLOCK | ";") ;

ASSIGNMENT = IDENTIFIER, "=", RELATIONAL_EXPRESSION, ";";

PRINTF = "printf", "(", RELATIONAL_EXPRESSION, ")", ";" ;

SCANF = "scanf", "(", ")" ;

IF_STATEMENT = "if", "(", RELATIONAL_EXPRESSION, ")", STATEMENT, [ "else", STATEMENT ] ;

WHILE_STATEMENT = "while", "(", RELATIONAL_EXPRESSION, ")", STATEMENT ;

EXPRESSION = TERM, { ("||" | "+","-"), TERM } ;

RELATIONAL_EXPRESSION = EXPRESSION, { ("==" | "<", ">"), EXPRESSION } ;

TERM = FACTOR, { ("*" | "/" | "&&"), FACTOR } ;

FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | "(", RELATIONAL_EXPRESSION, ")" | IDENTIFIER | SCANF;

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;

NUMBER = DIGIT, { DIGIT } ;

LETTER = ( a | ... | z | A | ... | Z ) ;

DIGIT = ( 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ) ;



![Alt text](diagrama.jpg)

![git status](http://3.129.230.99/svg/PedroPauloMorenoCamargo/Compilador/)
