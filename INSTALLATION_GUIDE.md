# Installation and workflow

Prerequisites: Git, Python 3.10 or newer, and `g++` on `PATH`. Python packages are declared in `pyproject.toml`; `pytest` is included in the `dev` extra.

## Windows PowerShell

```powershell
git clone https://github.com/GauravHmm/minipy-transpiler.git
cd minipy-transpiler
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -e ".[dev]"
python -m pytest -q
python -m minipy examples\input_demo.mp
g++ examples\input_demo.cpp -o examples\input_demo.exe
.\examples\input_demo.exe
```

If activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` for the current shell. Verify the compiler with `g++ --version`. When the final command pauses, type a line such as `Gaurav` and press Enter. MiniPy writes C++ only; `g++` produces the executable.

## Linux/macOS

```bash
git clone https://github.com/GauravHmm/minipy-transpiler.git
cd minipy-transpiler
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest -q
python -m minipy examples/input_demo.mp
g++ examples/input_demo.cpp -o examples/input_demo
./examples/input_demo
```

A fresh clone was not created during this audit; the commands match the project layout and were verified against the existing editable installation.
