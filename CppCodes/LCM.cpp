// Calculating least common multiple of several numbers.

#include <iostream>
#include <vector>
using namespace std;

int main()
{
    vector<int> v;
    int value;

    while(cin >> value)
        v.push_back(value);

    long long lcm;
    int ini;

    lcm = ini = v[0];

    for(size_t i = 0; i < v.size(); ++i) {
        while(lcm % v[i])
            lcm += ini;
        ini = lcm;
    }

    cout << "LCM: " << lcm << '\n';

    return 0;
}

