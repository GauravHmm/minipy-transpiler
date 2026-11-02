# MiniPy grammar

This grammar is reconstructed from `src/minipy/parser.py`; it describes MiniPy, not Python. `NEWLINE`, `INDENT`, and `DEDENT` are emitted by the lexer.

```ebnf
program          = { NEWLINE | statement }, EOF ;
statement        = assignment | print_stmt | if_stmt | while_stmt | for_stmt | function_def | return_stmt ;
assignment       = IDENTIFIER, "=", expression, NEWLINE ;
print_stmt       = "print", "(", expression, ")", NEWLINE ;
if_stmt          = "if", expression, ":", NEWLINE, INDENT, block, DEDENT, [ "else", ":", NEWLINE, INDENT, block, DEDENT ] ;
while_stmt       = "while", expression, ":", NEWLINE, INDENT, block, DEDENT ;
for_stmt         = "for", IDENTIFIER, "in", expression, ":", NEWLINE, INDENT, block, DEDENT ;
function_def     = "def", IDENTIFIER, "(", [ parameters ], ")", ":", NEWLINE, INDENT, block, DEDENT ;
parameters       = IDENTIFIER, { ",", IDENTIFIER } ;
return_stmt      = "return", [ expression ], NEWLINE ;
block            = { NEWLINE | statement } ;
expression       = logical_or ;
logical_or       = logical_and, { "or", logical_and } ;
logical_and      = comparison, { "and", comparison } ;
comparison       = additive, { comparison_operator, additive } ;
additive         = multiplicative, { ("+" | "-"), multiplicative } ;
multiplicative   = unary, { ("*" | "/" | "%"), unary } ;
unary            = [ "-" | "not" ], primary ;
primary          = NUMBER | STRING | "True" | "False" | IDENTIFIER, [ call_suffix ] | "range", call_suffix | "(", expression, ")" ;
call_suffix      = "(", [ expression, { ",", expression } ], ")" ;
comparison_operator = "<" | ">" | "<=" | ">=" | "==" | "!=" ;
```

`input()` is parsed by the `IDENTIFIER, call_suffix` production and recognized as a built-in by `SemanticAnalyzer.check_call()`. It takes no arguments and has type `string`.

Terminals include identifiers, numbers, strings, punctuation, the operators above, and keywords `print if else while for in range def return and or not True False`. Non-terminals are the named productions.

Precedence, highest to lowest: primary, unary, multiplicative, additive, comparison, `and`, then `or`. Repeated binary operators are left-associative. A chained comparison is nested left-to-right, unlike Python's special chained-comparison semantics. `/` is generated as a C++ `double` expression, including for integer operands.

`Lexer._handle_indentation()` uses an indentation stack: it emits `INDENT` on increased leading whitespace and one or more `DEDENT`s on decrease. Tabs count as one character; no fixed four-space rule or source coordinates are implemented.
