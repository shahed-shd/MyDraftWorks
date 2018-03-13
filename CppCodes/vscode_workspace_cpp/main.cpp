#include <cstdio>
using namespace std;


int main()
{
    freopen("in.txt", "r", stdin);
    //freopen("out.txt", "w", stdout);

    int n;
    scanf("%d", &n);

    int arr[20];

    for(int i = 0; i <= n; ++i) {
        arr[i] = i * 5;
    }

    int sum = 0;

    for(int i = 0; i <= n; ++i) {
        sum += arr[i];
    }

    printf("sum = %d\n", sum);

    return 0;
}