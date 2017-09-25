// this fn justifies if a number prime or not.

#include <iostream>
#include <cmath>
using namespace std;

bool is_prime(int n)
{
    if(n < 2) return 0;
    else if(n == 2) return 1;
    else if(n%2 == 0) return 0;

    int root = sqrt(n);

    for(int i = 3; i <= root; i += 2) {
        if(n % i == 0) return 0;
    }

    return 1;
}

int main()
{
    int n = 2147483647;

    if(is_prime(n)) cout << n << " is prime.\n";
    else cout << n << " is not prime.\n";

    return 0;
}
