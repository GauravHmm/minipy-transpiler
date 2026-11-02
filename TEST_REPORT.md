# Test report

Command executed on the current working tree:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Result: **35 passed in 1.15s**; 0 failed, 0 skipped. The pre-input baseline was 29 passing tests.

| Area | Evidence |
|---|---|
| Lexer | `test_input_is_recognized_as_a_callable_identifier` verifies `input` remains an identifier, preserving generic call parsing. |
| Parser | `test_input_call_expression` verifies `CallNode("input", [])`. |
| Semantics | `test_input_returns_a_string_and_rejects_arguments` verifies string inference and `input("Name")` rejection. |
| Code generation | Two tests verify helper generation, direct `print(input())`, assignment typing, and one helper for multiple calls. |
| Integration | `test_generated_input_program_compiles_and_reads_multiple_lines` generates C++, runs `g++`, executes it with two supplied lines, and checks exact output. |

Existing coverage in `tests/test_lexer.py`, `test_parser.py`, `test_semantic.py`, and `test_codegen.py` covers tokens, precedence, assignments, conditions, integer functions, range checks, type errors, strings, and generated fragments.

Important uncovered areas: CLI error output, malformed indentation/string cases, all loop runtime paths in automated tests, generated C++ compilation for every language feature, and known function-order/global-scope limitations.
