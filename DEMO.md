# Verified end-to-end demonstration

The reviewed program is `examples/input_demo.mp`:

```python
name = input()
message = "Hello, " + name
print(message)

counter = 0
while counter < 2:
    print(counter)
    counter = counter + 1

for index in range(2):
    print(index)

def square(number):
    return number * number

print(square(5))
```

Run from the repository root:

```powershell
.\.venv\Scripts\python.exe -m minipy examples\input_demo.mp
g++ examples\input_demo.cpp -o examples\input_demo.exe
"Gaurav" | .\examples\input_demo.exe
```

Verified output:

```text
Hello, Gaurav
0
1
0
1
25
```

The lexer starts with `IDENTIFIER(name) ASSIGN IDENTIFIER(input) LPAREN RPAREN`. The first AST node is `AssignmentNode(name='name', expression=CallNode(name='input', arguments=[]))`. Semantic analysis returns `True`: `input()` has type `string`, so `message` is a string concatenation.

Generated C++ contains this helper once only:

```cpp
std::string minipy_input() {
    std::string value;
    std::getline(std::cin, value);
    return value;
}
```

It translates the first assignment to `std::string name = minipy_input();`. `examples/multiple_input.mp` verifies two successive complete-line reads. Input `first line` then `second line` produced the same two lines as output.
