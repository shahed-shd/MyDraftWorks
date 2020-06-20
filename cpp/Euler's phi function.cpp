#include <cstdio>
#include <bitset>
#include <cmath>
#include <vector>
using namespace std;

const int MAXN = 50000+3;

int phi[MAXN] = {0, 1};     // phi(1) = 1.

bitset<MAXN> status;
vector<int> primes;

void sieve()
{
    for(int i = 4; i < MAXN; i+=2) status[i] = true;

    int rt = sqrt(MAXN);

    for(int i = 3; i <= rt; i+=2)
        if(!status[i])
            for(int j = i*i; j < MAXN; j += i<<1)
                status[j] = true;

    primes.push_back(2);

    for(int i = 3; i < MAXN; i+=2)
        if(!status[i]) primes.push_back(i);
}

int calc_phi(int n)
{
    if(phi[n]) return phi[n];
    if(!status[n]) return phi[n] = n-1;

    int& ans = phi[n];

    ans = n;

    for(int i = 0; primes[i]*primes[i] <= n; ++i) {
        if(n % primes[i] == 0) {
            //ans /= primes[i];
            //ans *= primes[i]-1;
            ans -= ans / primes[i];     // The above two lines are alternative to this line.

            while(n % primes[i] == 0)
                n /= primes[i];
        }
    }

    if(n != 1) {
        ans /= n;
        ans *= n-1;
    }

    return ans;
}

int main()
{
    sieve();

    int n;

    while(scanf("%d", &n), n != 0 && n < MAXN)
        printf("phi(%d) = %d\n", n, calc_phi(n));

    return 0;
}
