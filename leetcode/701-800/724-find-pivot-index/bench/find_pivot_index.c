// LeetCode #724: Find Pivot Index -- the total, then one running sum.
// Benchmark mirror of the Kara star arm: the total once, then a walk
// from the left keeping the sum of the numbers passed, stopping at the
// first index whose left sum equals what is left on the right.
#include <stdint.h>
#include <stdio.h>

enum { ARRAYS = 50, LEN = 9999 };

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t pivot_index(const int64_t *nums, int64_t n) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) total += nums[i];
    int64_t left = 0;
    for (int64_t i = 0; i < n; i++) {
        if (left == total - left - nums[i]) return i;
        left += nums[i];
    }
    return -1;
}

int main(void) {
    int64_t seed = 724;
    static int64_t arrays[ARRAYS][LEN];
    for (int k = 0; k < ARRAYS; k++) {
        for (int j = 0; j < 4999; j++) arrays[k][j] = next_random(&seed) % 2001 - 1000;
        arrays[k][4999] = next_random(&seed) % 2001 - 1000;
        for (int j = 0; j < 4999; j++) arrays[k][5000 + j] = arrays[k][4998 - j];
    }
    int64_t sum = 0;
    for (int64_t round = 0; round < 1000; round++)
        for (int64_t k = 0; k < ARRAYS; k++) {
            int64_t p = (round * 7919 + k * 31) % LEN;
            arrays[k][p] = -arrays[k][p];
            sum += pivot_index(arrays[k], LEN);
        }
    printf("1000 rounds of 50 arrays of 9999 numbers: sum %lld\n", (long long)sum);
    return 0;
}
