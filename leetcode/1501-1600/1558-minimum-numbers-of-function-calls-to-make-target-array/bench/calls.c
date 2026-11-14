// LeetCode #1558: Minimum Numbers of Function Calls to Make Target Array --
// bench: the ★ arm (every value's 1 bits, and the widest value's length
// less one) over 20 arrays of 100000 values, built once, each asked 30
// times. C mirror of calls.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t min_operations(const int64_t *nums, int64_t n) {
    int64_t increments = 0, widest = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        increments += __builtin_popcountll((uint64_t)x);
        if (x > 0) {
            int64_t length = 64 - __builtin_clzll((uint64_t)x);
            if (length > widest) widest = length;
        }
    }
    return increments + (widest - 1 > 0 ? widest - 1 : 0);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1558;
    static int64_t *arrays[20];
    for (int a = 0; a < 20; a++) {
        arrays[a] = malloc(N * sizeof(int64_t));
        for (int64_t i = 0; i < N; i++) {
            int64_t bits = next_random(&seed) % 30 + 1;
            int64_t draw = next_random(&seed) * 32768;
            draw += next_random(&seed);
            arrays[a][i] = draw % ((int64_t)1 << bits);
        }
    }
    int64_t check = 0, total = 0;
    for (int pass = 0; pass < 30; pass++) {
        for (int a = 0; a < 20; a++) {
            int64_t calls = min_operations(arrays[a], N);
            total += calls;
            check = mix(check, calls);
        }
    }
    printf("30 passes over 20 arrays of 100000 values: %lld calls, checksum %lld\n",
           (long long)total, (long long)check);
    for (int a = 0; a < 20; a++) free(arrays[a]);
    return 0;
}
