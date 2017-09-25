// finding the sub array of maximum sum
// by Kadane's Algorithm.

// reference link:
// http://www.algorithmist.com/index.php/Kadane%27s_Algorithm
// http://codeforces.com/blog/entry/13713
// http://www.geeksforgeeks.org/largest-sum-contiguous-subarray/

#include <iostream>
using namespace std;

void maxSubArraySum(int *arr, int sz, int &maxSum, int &maxStartIndex, int &maxEndIndex)
{
    maxSum = -2147483647;
    maxStartIndex = maxEndIndex = 0;

    int currentMaxSum, currentStartIndex, currentEndIndex;

    currentMaxSum = currentStartIndex = 0;

    for(currentEndIndex = 0; currentEndIndex < sz; ++currentEndIndex) {
        currentMaxSum += arr[currentEndIndex];

        if(currentMaxSum > maxSum) {
            maxSum = currentMaxSum;
            maxStartIndex = currentStartIndex;
            maxEndIndex = currentEndIndex;
        }

        if(currentMaxSum < 0) {
            currentMaxSum = 0;
            currentStartIndex = currentEndIndex + 1;
        }
    }
}


// Driver program to test maxSubArray.
int main()
{
    int arr[] = {-2, -3, -4, -1, -2, -1, -5, -3};

    int n = sizeof(arr) / sizeof(arr[0]);

    int maxSum, maxStartIndex, maxEndIndex;

    maxSubArraySum(arr, n, maxSum, maxStartIndex, maxEndIndex);

    cout << maxSum << ' ' << maxStartIndex << ' ' << maxEndIndex << '\n';

    return 0;
}

