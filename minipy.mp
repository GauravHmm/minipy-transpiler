
# MiniPy comprehensive demonstration

# 1. Variables and arithmetic
a = 10
b = 3
result = a + b * 2
print("Arithmetic result:")
print(result)

# 2. Reassignment
result = result + 5
print("After reassignment:")
print(result)

# 3. Conditional statement
if result > 20:
    print("Result is greater than 20")
else:
    print("Result is 20 or less")

# 4. While loop
print("While loop:")
i = 0
while i < 3:
    print(i)
    i = i + 1

# 5. For loop using range
print("For loop:")
for j in range(4):
    print(j)

# 6. Function with return value
def square(n):
    return n * n

print("Square of 5:")
print(square(5))
