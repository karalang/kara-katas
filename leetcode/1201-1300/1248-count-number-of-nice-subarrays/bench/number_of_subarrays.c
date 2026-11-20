// LeetCode #1248 bench, in C: the ★ arm (prefix counts of odd values in
// an array indexed by count) on 50 random arrays of 50000 values built
// once, each with its own chance of an odd value, each asked with 10
// random k; every answer folded into a checksum.

#include <stdio.h>
#include <string.h>

#define N 50000
#define ARRAYS 50

static long long seed = 1248;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long prefixes[N + 1];

static long long number_of_subarrays(const long long *nums, int n, long long k) {
    memset(prefixes, 0, sizeof(long long) * (n + 1));
    prefixes[0] = 1;
    long long odd = 0, nice = 0;
    for (int i = 0; i < n; i++) {
        odd += nums[i] % 2;
        if (odd >= k) nice += prefixes[odd - k];
        prefixes[odd]++;
    }
    return nice;
}

static long long arrays[ARRAYS][N];

int main(void) {
    for (int a = 0; a < ARRAYS; a++) {
        long long percent = next_random() % 101;
        for (int i = 0; i < N; i++) {
            long long v = next_random() % 50000 + 1;
            arrays[a][i] = next_random() % 100 < percent ? 2 * v - 1 : 2 * v;
        }
    }
    long long check = 0;
    for (int a = 0; a < ARRAYS; a++) {
        long long odd = 0;
        for (int i = 0; i < N; i++) odd += arrays[a][i] % 2 == 1;
        for (int r = 0; r < 100; r++) {
            long long k = next_random() % (odd + 1) + 1;
            check = (check * 131 + number_of_subarrays(arrays[a], N, k)) % 1000000007;
        }
    }
    printf("50 arrays of 50000 values, 100 k each: checksum %lld\n", check);
    return 0;
}
