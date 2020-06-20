/*

Suppose, an 3D array has R rows, C columns & D depth like
int table[R][C][D]
and accessing an element of i-th row, j-th coumn, k-th depth like
table[i][j][k]

is similar to

declaring a pointer like
int *ptr = new int [R*C*D]
and accessing an element of i-th row, j-th coumn, k-th depth like
*(table + (C*i+j)*D + k)

*/


#include <iostream>
using namespace std;

#define     tbl(i,j,k)    (*(tbl + (C*i+j)*D + k))
//#define     table(i,j,k)    *( *( *(table + i) + j) + k)

int main()
{
    int R, C, D;

    R = 5;
    C = 6;
    D = 7;

    int table[R][C][D];

    int i, j, k;

    i = 1;
    j = 2;
    k = 3;

    int* tbl = (int*) (table);

    table[i][j][k] = 1437;

    cout << tbl(i, j, k) << '\n';

    cout << *(*(*(table+i) + j) + k) << '\n';

    return 0;
}
