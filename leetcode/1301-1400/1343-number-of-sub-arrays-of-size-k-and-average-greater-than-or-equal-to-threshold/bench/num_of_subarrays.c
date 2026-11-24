// LeetCode #1343 bench in C: the ★ arm (a sliding window of the last k
// values, counted when its sum reaches k * threshold) on the same 10
// arrays of 10^5 values and 60 passes.
#include <stdint.h>
#include <stdio.h>

static int num_of_subarrays(const int *arr, int n, int k, int threshold) {
    int need = k * threshold;
    int sum = 0, count = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
        if (i >= k) sum -= arr[i - k];
        if (i >= k - 1 && sum >= need) count++;
    }
    return count;
}

static int64_t seed = 1343;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { N = 100000 };
    static int arrays[10][N];
    for (int a = 0; a < 10; a++)
        for (int i = 0; i < N; i++) arrays[a][i] = (int)(1 + next_random() % 10000);
    int64_t check = 0;
    for (int64_t pass = 0; pass < 60; pass++) {
        for (int a = 0; a < 10; a++) {
            arrays[a][check % N] = (int)(1 + (check / 7) % 10000);
            int k = (int)(1 + check % 1000);
            int threshold = (int)(4500 + check % 400);
            int answer = num_of_subarrays(arrays[a], N, k, threshold);
            check = (check * 31 + answer + pass) % 1000000007;
        }
    }
    printf("60 passes over 10 arrays of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
