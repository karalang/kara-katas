// LeetCode #718: Maximum Length of Repeated Subarray -- one rolling row.
// Benchmark mirror of the Kara star arm: the length of the common run
// ending at each pair of places, one row at a time, walked downwards.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t find_length(const int64_t *nums1, int64_t m, const int64_t *nums2, int64_t n) {
    int64_t *run = calloc(n + 1, sizeof(int64_t));
    int64_t best = 0;
    for (int64_t i = 1; i <= m; i++) {
        for (int64_t j = n; j >= 1; j--) {
            if (nums1[i - 1] == nums2[j - 1]) {
                run[j] = run[j - 1] + 1;
                if (run[j] > best) best = run[j];
            } else {
                run[j] = 0;
            }
        }
    }
    free(run);
    return best;
}

enum { ARRAYS = 60, N = 1000 };

int main(void) {
    int64_t seed = 718;
    static int64_t arrays[ARRAYS][N];
    for (int a = 0; a < ARRAYS; a++)
        for (int i = 0; i < N; i++) arrays[a][i] = next_random(&seed) % 10;
    int64_t sum = 0;
    for (int round = 0; round < 40; round++)
        for (int k = 0; k < 20; k++)
            sum += find_length(arrays[k], N, arrays[(k + round + 1) % ARRAYS], N);
    printf("40 rounds of 20 pairs of 1000 numbers: sum %lld\n", (long long)sum);
    return 0;
}
