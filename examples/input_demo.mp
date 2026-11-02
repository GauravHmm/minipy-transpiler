# Review demonstration: input, strings, control flow, loops, and functions.
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
