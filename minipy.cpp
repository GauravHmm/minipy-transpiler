#include <iostream>
#include <string>

int square(int n) {
    return (n * n);
    return 0;
}

int main() {
    int a = 10;
    int b = 3;
    int result = (a + (b * 2));
    std::cout << "Arithmetic result:" << std::endl;
    std::cout << result << std::endl;
    result = (result + 5);
    std::cout << "After reassignment:" << std::endl;
    std::cout << result << std::endl;
    if ((result > 20)) {
        std::cout << "Result is greater than 20" << std::endl;
    } else {
        std::cout << "Result is 20 or less" << std::endl;
    }
    std::cout << "While loop:" << std::endl;
    int i = 0;
    while ((i < 3)) {
        std::cout << i << std::endl;
        i = (i + 1);
    }
    std::cout << "For loop:" << std::endl;
    for (int j = 0; j < 4; j += 1) {
        std::cout << j << std::endl;
    }
    std::cout << "Square of 5:" << std::endl;
    std::cout << square(5) << std::endl;
    return 0;
}
