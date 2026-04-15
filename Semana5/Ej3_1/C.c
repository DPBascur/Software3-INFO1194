#include <stdio.h>

int main() {
    int n, suma = 0;
    printf("Introduce un número positivo: ");
    scanf("%d", &n);
    if (n < 1) {
        printf("Por favor, introduce un número positivo.\n");
        return 1;
    } else {
        printf("Calculando la sumatoria de 1 a %d...\n", n);
            for (int i = 1; i <= n; i++) {
        suma += i;
    }
        printf("La sumatoria de 1 a %d es: %d\n", n, suma);
    }


    return 0;
}