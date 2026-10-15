
import sys
from pathlib import Path

from minipy.lexer import Lexer
from minipy.parser import Parser
from minipy.semantic import SemanticAnalyzer
from minipy.codegen import CodeGenerator


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m minipy <source.mp>")
        sys.exit(1)

    source_file = Path(sys.argv[1])

    if not source_file.exists():
        print(f"Error: File '{source_file}' not found.")
        sys.exit(1)

    try:
        # Read the MiniPy source code.
        source = source_file.read_text(encoding="utf-8")

        # Stage 1: Lexical analysis.
        tokens = Lexer(source).tokenize()

        # Stage 2: Syntax analysis.
        program = Parser(tokens).parse()

        # Stage 3: Semantic analysis.
        analyzer = SemanticAnalyzer()
        analyzer.analyze(program)

        # Stage 4: Generate C++.
        generator = CodeGenerator()
        cpp_code = generator.generate(program)

        # Save the generated C++ beside the source file.
        output_file = source_file.with_suffix(".cpp")
        output_file.write_text(cpp_code, encoding="utf-8")

        print(f"C++ code generated successfully: {output_file}")

    except (SyntaxError, ValueError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
