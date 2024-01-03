#include <stdio.h>
#include "utils.h"

int main() {
    int a = 2, b = 3;

    int sum = add(a, b);
    printf("sum: %d\n", sum);

    int product = multiply(a, b);
    printf("product: %d\n", product);

    return 0;
}
