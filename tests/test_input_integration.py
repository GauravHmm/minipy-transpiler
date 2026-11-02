import shutil
import subprocess
from pathlib import Path

import pytest

from minipy.codegen import CodeGenerator
from minipy.lexer import Lexer
from minipy.parser import Parser
from minipy.semantic import SemanticAnalyzer


def transpile(source):
    program = Parser(Lexer(source).tokenize()).parse()
    SemanticAnalyzer().analyze(program)
    return CodeGenerator().generate(program)


@pytest.mark.skipif(shutil.which("g++") is None, reason="g++ is required")
def test_generated_input_program_compiles_and_reads_multiple_lines():
    cpp_code = transpile(
        "first = input()\n"
        "second = input()\n"
        "print(first)\n"
        "print(second)"
    )
    build_dir = Path(".pytest_cache") / "input_integration"
    build_dir.mkdir(parents=True, exist_ok=True)
    cpp_file = build_dir / "input_program.cpp"
    executable = build_dir / "input_program.exe"
    cpp_file.write_text(cpp_code, encoding="utf-8")

    subprocess.run(
        ["g++", str(cpp_file), "-o", str(executable)],
        check=True,
        capture_output=True,
        text=True,
    )
    result = subprocess.run(
        [str(executable)],
        input="Gaurav\nMiniPy\n",
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout == "Gaurav\nMiniPy\n"
