// LeetCode #2366: Minimum Replacements to Sort the Array -- the bench, the
// ★ arm in C: greedy from the right, a value over the bound split into
// the fewest pieces that fit, the bound becoming the smallest piece of
// the most even split.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t minimum_replacement(const int64_t *nums, int64_t n) {
    int64_t bound = nums[n - 1];
    int64_t ops = 0;
    for (int64_t i = n - 2; i >= 0; i--) {
        int64_t v = nums[i];
        if (v <= bound) {
            bound = v;
        } else {
            int64_t k = (v + bound - 1) / bound;
            ops += k - 1;
            bound = v / k;
        }
    }
    return ops;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // array a: 10^5 values from 1 to 10^(a - 1) when a > 0, and a falling
    // run from 10^9 when a is 0
    const int64_t n = 100000;
    int64_t seed = 2366;
    int64_t *arrays[10];
    int64_t top = 1;
    for (int64_t a = 0; a < 10; a++) {
        arrays[a] = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            if (a == 0) {
                arrays[a][i] = 1000000000 - i * 9999;
            } else {
                int64_t hi = next_random(&seed);
                arrays[a][i] = 1 + (hi * 32768 + next_random(&seed)) % top;
            }
        }
        if (a > 0) {
            top *= 10;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 100; p++) {
        for (int a = 0; a < 10; a++) {
            check = (check * 31 + minimum_replacement(arrays[a], n) % 1000000007 + p) % 1000000007;
        }
    }
    printf("100 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) {
        free(arrays[a]);
    }
    return 0;
}
