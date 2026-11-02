# Viva preparation

## Short introduction

MiniPy is a Python-to-C++ source-to-source transpiler made to demonstrate compiler stages: lexing, recursive-descent parsing, AST construction, semantic checking, and C++ generation. It supports a deliberately constrained Python-like language and now includes zero-argument string `input()`.

## Two-minute script

“MiniPy accepts a `.mp` file and translates it into C++. The lexer converts characters to tokens, including indentation tokens. The parser consumes these tokens using recursive-descent functions and builds dataclass AST nodes. Semantic analysis checks variables, types, scopes, functions, `range`, and built-in `input`. Finally, the generator writes C++ with `main`, control flow, and functions. For input, it emits one `std::getline` helper that returns `std::string`. MiniPy itself does not create machine code; `g++` compiles the generated C++. The test suite currently has 35 passing tests, including an input compile-and-run integration test.”

## Five-minute technical outline

1. State the problem: demonstrate a complete, inspectable compiler pipeline for a controlled language.
2. Show the pipeline diagram in `TECHNICAL_AUDIT.md` and `examples/input_demo.mp`.
3. Explain tokenization and the indentation stack in `Lexer._handle_indentation`.
4. Explain parser precedence methods and AST dataclasses.
5. Explain semantic variable maps, local function scope, and function registration.
6. Show C++ generation and the `minipy_input` helper.
7. Run the demo, tests, and discuss the limitations honestly.

## Likely questions and accurate answers

1. **Why transpile rather than interpret?** It demonstrates compilation phases while allowing `g++` to handle native compilation.
2. **What parser is used?** A hand-written recursive-descent parser with layered precedence methods.
3. **How does MiniPy handle blocks?** Lexer emits `INDENT` and `DEDENT`; parser's `block()` reads until dedent.
4. **Why use an AST?** It isolates syntax representation from semantic checks and output generation.
5. **How are variable types obtained?** From literals and expression structure; maps retain each variable type.
6. **How does `input()` work?** It is a generic call node, semantically a zero-argument string built-in, generated as `minipy_input()` using `std::getline`.
7. **Why no `input(prompt)`?** Prompts and numeric conversion are outside the deliberately minimal scope.
8. **How are arithmetic priorities implemented?** Parser functions call tighter-precedence functions.
9. **Why is `range` restricted?** Generation emits only an increasing integer C++ loop; step must be a positive literal.
10. **What does semantic analysis reject?** Undefined variables/functions, type changes, invalid conditions, bad function calls, invalid range calls, and invalid input arguments.
11. **Does MiniPy compile C++?** No; the user runs `g++` separately.
12. **How are strings emitted?** The generator escapes backslashes, quotes, newlines, and tabs.
13. **Are functions fully general?** No; parameters and results are restricted to integer-compatible values.
14. **Is division Python division?** It emits a C++ double division expression.
15. **Are conditions truthy like Python?** No; they require bool/unknown types.
16. **Are chained comparisons Python-equivalent?** No; they become nested binary comparisons.
17. **Can local block variables escape?** No; semantic checking removes newly created block names after the block.
18. **Does it report line/column positions?** No.
19. **How is forward calling handled?** Top-level calls to later functions work; calls from one generated function to a later function lack C++ prototypes and fail compilation.
20. **What is the complexity?** Each phase is linear in source/tokens/AST nodes under average constant-time dictionary lookup.

## Challenging questions

- Why does a function's read of a top-level MiniPy variable pass semantics but fail generated C++? Functions are emitted before `main`, where top-level variables are declared.
- Why does generated function order matter? No forward C++ declarations are emitted.
- Why is an unreachable `return 0;` emitted after a return? `generate_function()` always appends a default C++ return.
- What would numeric input require? Explicit conversion built-ins, semantic rules, and defined runtime handling of invalid text.
- What should be fixed first? Add C++ prototypes and make global-variable semantics agree with the generated C++ scope.
