# Compilador – A Tiny C‑like Compiler in Python

> • **Language:** Python 3

Compilador is a didactic compiler for a small, C‑inspired language.  
Depending on the branch you check out, it will either **interpret** the source program on the fly (`main`) or **compile** it to a simplified assembly listing (`assembly`).

| Branch      | Behaviour                            | Output                                                          |
|-------------|--------------------------------------|-----------------------------------------------------------------|
| `main`      | Parses & **executes** the program    | Runs immediately, printing any `printf` output to the console   |
| `assembly`  | Parses & **generates assembly code** | Creates a `<source>.asm` file with low‑level instructions       |


## Language Features

* **Variables & Types** – `int` and `str`, optional initialisation  
  ```c
  int a = 5, b;
  str  name = "Alice";
  ```
* **Expressions & Operators** – arithmetic `+ - * /`, relational `== < >`, logical `&& ||`
* **Control Flow** – `if` / `else` conditionals and `while` loops  
  ```c
  if (a < 10) { … } else { … }
  while (condition) { … }
  ```
* **I/O** – `printf(expr);` for output and a stub `scanf();` for input
* **Blocks** – statements grouped inside `{ … }`
* **Semicolons** – every statement ends with `;` (except block headers)


## EBNF Grammar

```ebnf
PROGRAM              = { STATEMENT } ;

STATEMENT            = ( ASSIGNMENT
                       | DECLARATION
                       | PRINTF
                       | IF_STATEMENT
                       | WHILE_STATEMENT
                       | BLOCK
                       | ";"                     ) ;

BLOCK                = "{", { STATEMENT }, "}" ;

DECLARATION          = TYPE, IDENT_DECL, ";" ;
IDENT_DECL           = IDENTIFIER, [ "=", EXPR ]
                       { ",", IDENTIFIER, [ "=", EXPR ] } ;

ASSIGNMENT           = IDENTIFIER, "=", EXPR, ";" ;

PRINTF               = "printf", "(", EXPR, ")", ";" ;

SCANF                = "scanf", "(", ")",          (* no arguments *) ;

IF_STATEMENT         = "if", "(", EXPR, ")", STATEMENT,
                       [ "else", STATEMENT ] ;

WHILE_STATEMENT      = "while", "(", EXPR, ")", STATEMENT ;

EXPR                 = TERM, { ("||" | "+" | "-"), TERM } ;
TERM                 = FACTOR, { ("*" | "/" | "&&"), FACTOR } ;
FACTOR               = ( ("+" | "-" | "!"), FACTOR )
                     | NUMBER
                     | STRING
                     | IDENTIFIER
                     | SCANF
                     | "(", EXPR, ")" ;

TYPE                 = "int" | "str" ;
IDENTIFIER           = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER               = DIGIT, { DIGIT } ;

LETTER               = "A" … "Z" | "a" … "z" ;
DIGIT                = "0" … "9" ;
STRING               = """, { CHARACTER }, """ ;
CHARACTER            = LETTER | DIGIT | SYMBOL ;
SYMBOL               = " " | "!" | "@" | "#" | "$" | "%" | "^" | "&"
                       | "*" | "(" | ")" | "-" | "_" | "+" | "="
                       | "{" | "}" | "[" | "]" | ":" | ";" | "'" | "<"
                       | ">" | "," | "." | "?" | "/" | "\" | "|" ;
```

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/PedroPauloMorenoCamargo/Compilador.git
cd Compilador
```

### 2. Requirements

* Python 3 (no external libraries needed).

### 3. Write or edit your source file

A sample program lives in **`teste.c`**. Edit it or create a new `myprog.c`.

### 4. Run – main branch (interpreter)

```bash
# interpret default teste.c
python main.py

# or pass an explicit source file if main.py supports it
python main.py myprog.c
```

The program executes immediately; any `printf` statements print to the console.

### 5. Run – assembly branch

```bash
git checkout assembly
python main.py            # generates teste.asm (or <file>.asm)
```

Open the resulting `.asm` file to inspect the low‑level code.  
Assembling & running this output is left to you (target dialect is illustrative).

---

## Example

```c
int i = 0;
while (i < 5) {
    printf(i);
    i = i + 1;
}
```
*Main branch output:*
```
0
1
2
3
4
```

---

## Repository Layout (main branch)

```
.
├── lexer.py       # token definitions
├── parser.py      # recursive‑descent parser -> AST
├── ast.py         # node classes
├── interpreter.py # AST walker / runtime
├── main.py        # entry point
└── teste.c        # sample source program
```

Assembly branch swaps `interpreter.py` for `codegen_asm.py` that walks the AST
and emits assembly instead.


