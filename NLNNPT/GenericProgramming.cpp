#include <iostream>
using namespace std;


template <typename T>
T findMax(T a, T b) {
    return (a > b) ? a : b;
}

int main() {
    cout << "Max of 3 and 7: " << findMax(3, 7) << endl;       // int
    cout << "Max of 3 and 7: " << findMax(10.0, 10.0) << endl;
    cout << "Max of 5.5 and 2.3: " << findMax(5.5, 2.3) << endl; // double
    cout << "Max of 'A' and 'Z': " << findMax('A', 'Z') << endl; // char
    return 0;
}

