# MiniPy Transpiler

MiniPy is a small Compiler Design project that converts a simple Python-like
language (`.mp` files) into C++ source code (`.cpp` files). It demonstrates a
complete compiler pipeline: lexer, parser, abstract syntax tree (AST), semantic
analysis, and C++ code generation.

## What MiniPy does

Run `python -m minipy sample.mp` to read MiniPy source, validate it, and write
`sample.cpp` beside the input file. MiniPy generates C++ only; it does not
automatically compile or execute the generated program.

## Supported language features

- Integer and decimal number literals, strings, and `True` / `False`
- Variables, reassignment with the same type, arithmetic, comparisons, and
  boolean `and`, `or`, and `not`
- `print(expression)`
- Indented `if` / `else`, `while`, and `for item in range(...)` blocks
- Integer-only functions with integer parameters and integer return values
- Comments beginning with `#` and escaped string characters such as `\"`,
  `\\`, `\n`, and `\t`

## Technologies used

- Python 3.10+ for the transpiler and tests
- `pytest` for automated tests
- C++ and `g++` for compiling generated output

## Project structure

```text
src/minipy/       Compiler stages and command-line entry point
tests/            pytest tests for the lexer, parser, semantics, and generator
sample.mp         Example MiniPy input
sample.cpp        Example generated C++ output
pyproject.toml    Project and test configuration
```

## Setup on Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -e ".[dev]"
```

If PowerShell blocks activation, run this once for the current shell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Run the transpiler

```powershell
python -m minipy sample.mp
```

The command reports syntax or semantic errors clearly and writes `sample.cpp`.

## Compile and run the generated C++

```powershell
g++ sample.cpp -o sample.exe
.\sample.exe
```

For this MiniPy input:

```python
x = 10 + 20
print(x)
```

the generated program prints:

```text
30
```

## Run the tests

```powershell
python -m pytest -q
```

## Current limitations

- MiniPy is intentionally a small language, not full Python.
- Function parameters and return values are limited to integers.
- `for` loops support only `range(start)`, `range(start, stop)`, and
  `range(start, stop, step)` with a positive integer literal step.
- A variable first declared inside an `if`, `while`, or `for` block cannot be
  used outside that block. This conservative rule keeps generated C++ scopes
  safe and easy to explain.
- There are no lists, dictionaries, classes, input, `elif`, or standalone
  function-call statements.
