#include <iostream>
#include <string>

std::string minipy_input() {
    std::string value;
    std::getline(std::cin, value);
    return value;
}

int square(int number) {
    return (number * number);
    return 0;
}

int main() {
    std::string name = minipy_input();
    std::string message = ("Hello, " + name);
    std::cout << message << std::endl;
    int counter = 0;
    while ((counter < 2)) {
        std::cout << counter << std::endl;
        counter = (counter + 1);
    }
    for (int index = 0; index < 2; index += 1) {
        std::cout << index << std::endl;
    }
    std::cout << square(5) << std::endl;
    return 0;
}
