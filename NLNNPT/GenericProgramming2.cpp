#include <iostream>

template <typename T>
T findMax(T arr[], int size) {
    T maxVal = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > maxVal) {
            maxVal = arr[i];
        }
    }
    return maxVal;
}

int main() {
    int intArr[] = {1, 5, 3, 7, 9};
    double doubleArr[] = {2.5, 3.7, 1.8, 9.2, 5.4};
    char charArr[] = {'a', 'z', 'b', 'm'};

    std::cout << "Max in intArr: " << findMax(intArr, 5) << std::endl;
    std::cout << "Max in doubleArr: " << findMax(doubleArr, 5) << std::endl;
    std::cout << "Max in charArr: " << findMax(charArr, 4) << std::endl;

    return 0;
}

