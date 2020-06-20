#include <cstdio>
#include <cstdlib>
using namespace std;


int MAXVAL = 10;


inline int rand_range(int a, int b)     // a to b inclusive.
{
    return a + rand() % (b - a + 1);
}


int main()
{
    // freopen("in.txt", "w", stdout);

    int n = 10;
    printf("%d\n", n);

    for(int i = 0; i < n; ++i) {
        if(i) putchar(' ');
        printf("%d", rand_range(1, MAXVAL));
    }

    return 0;
}