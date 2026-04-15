#include <iostream>
using namespace std;

int main() {
    int n, suma = 0;
    cout << "Introduce un número positivo: ";
    cin >> n;
    if (n < 1) {
        cout << "Por favor, introduce un número positivo." << endl;
        return 1;
    } else {
        cout << "Calculando la sumatoria de 1 a " << n << "..." << endl;
        for (int i = 1; i <= n; i++) {
            suma += i;
        }
        cout << "La sumatoria de 1 a " << n << " es: " << suma << endl;
    }
    return 0;
}