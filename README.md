# Compilador — A C‑like Language Compiler/Interpreter in Python

> **Implementation language:** Python 3 (standard library only)

---

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Language Features](#language-features)  
3. [EBNF Grammar](#ebnf-grammar)  
4. [Repository Structure](#repository-structure)  
5. [Getting Started](#getting-started)  
6. [Examples](#examples)  
7. [Implementation Notes](#implementation-notes)  
8. [Branches](#branches)  

---

## Project Overview
**Compilador** is a didactic compiler for a **C‑inspired language**.  
The `main` branch **parses and executes** programs directly (interpreter), while the
`assembly` branch **translates the same language into a simplified assembly listing**.

---

## Language Features
| Category        | Supported syntax |
|-----------------|------------------|
| **Types**       | `int`, `str`, `void` |
| **Declarations**| `int x = 3, y;` · `str name = "Alice";` |
| **Assignments** | `x = x + 1;` |
| **Expressions** | `+ - * / == != < > && || !` (with precedence) |
| **Control flow**| `if (cond) stmt [else stmt]` · `while (cond) stmt` |
| **Functions**   | `int sum(int a,int b){…}` · `void main(){…}` |
| **I/O**         | `printf(expr);` · `scanf();` |
| **Comments**    | `/* … */` are stripped |
| **Empty stmt**  | bare `;` (no‑op) |

---

## EBNF Grammar
```ebnf
PROGRAM         = { FUNC_DECL } FUNC_CALL ";" ;

FUNC_DECL       = FUNC_TYPE IDENTIFIER
                  "(" [ PARAM_LIST ] ")" BLOCK ;

FUNC_TYPE       = "int" | "str" | "void" ;

PARAM_LIST      = PARAM { "," PARAM } ;
PARAM           = TYPE IDENTIFIER ;

BLOCK           = "{" { STATEMENT } "}" ;

STATEMENT       = DECLARATION
                | ASSIGNMENT
                | FUNC_CALL ";"
                | PRINTF_STMT
                | RETURN_STMT
                | IF_STMT
                | WHILE_STMT
                | BLOCK
                | ";" ;

DECLARATION     = TYPE DECL_ITEM { "," DECL_ITEM } ";" ;
DECL_ITEM       = IDENTIFIER [ "=" EXPR ] ;

ASSIGNMENT      = IDENTIFIER "=" EXPR ";" ;

FUNC_CALL       = IDENTIFIER "(" [ ARG_LIST ] ")" ;
ARG_LIST        = EXPR { "," EXPR } ;

PRINTF_STMT     = "printf" "(" EXPR ")" ";" ;

RETURN_STMT     = "return" EXPR ";" ;

IF_STMT         = "if" "(" EXPR ")" STATEMENT
                  [ "else" STATEMENT ] ;

WHILE_STMT      = "while" "(" EXPR ")" STATEMENT ;

EXPR            = COMP_EXPR ;

COMP_EXPR       = ADD_OR_EXPR [ REL_OP ADD_OR_EXPR ] ;
REL_OP          = "==" | "!=" | "<" | ">" ;

ADD_OR_EXPR     = TERM_AND_EXPR { ("+" | "-" | "||") TERM_AND_EXPR } ;
TERM_AND_EXPR   = FACTOR { ("*" | "/" | "&&") FACTOR } ;

FACTOR          = ( "+" | "-" | "!" ) FACTOR
                | NUMBER
                | STRING
                | IDENTIFIER [ FUNC_CALL_TAIL ]
                | "scanf" "(" ")"
                | "(" EXPR ")" ;

FUNC_CALL_TAIL  = "(" [ ARG_LIST ] ")" ;

TYPE            = "int" | "str" ;

IDENTIFIER      = LETTER { LETTER | DIGIT | "_" } ;
NUMBER          = DIGIT { DIGIT } ;
STRING          = '"' { CHARACTER } '"' ;

LETTER          = "A" … "Z" | "a" … "z" ;
DIGIT           = "0" … "9" ;
CHARACTER       = LETTER | DIGIT | SYMBOL ;
SYMBOL          = any visible printable character except '"' and control chars ;


```

---

## Repository Structure
```
.
├── arvore.py      # AST nodes & symbol tables
├── classes.py     # pre‑processor, tokenizer, parser
├── main.py        # CLI entry point
├── teste.c        # sample program
└── (assembly branch adds codegen_asm.py)
```

---

## Getting Started
### 1 · Prerequisites
* Python 3.8+ (no external deps)

### 2 · Clone
```bash
git clone https://github.com/PedroPauloMorenoCamargo/Compilador.git
cd Compilador
```

### 3 · Write a program
Edit **`teste.c`** or create `myprog.c`.

### 4 · Run (interpreter)
```bash
python main.py myprog.c
```
The program executes immediately; `printf` outputs appear in the console.

---

## Examples
### Loop
```c
int i = 0;
while (i < 5) {
    printf(i);
    i = i + 1;
}
```
_Output_
```
0
1
2
3
4
```

### Functions
```c
int sum(int a, int b) {
    return a + b;
}

void main() {
    int r = sum(2, 3);
    printf(r);
}
```
_Output_
```
5
```

---

## Implementation Notes
* **Type checks** — enforces `int`, `str`, `bool`; allows implicit `bool→int`.
* **Short‑circuit** — `&&`, `||` stop evaluation early.
* **Return** — implemented with an internal `ReturnException`.
* **Scoping** — each function call gets its own `SymbolTable`.

---

## Branches
* **`main`** — builds an AST and **runs** the program.  
* **`assembly`** — identical front‑end but **emits a `.asm` file** instead of executing.
