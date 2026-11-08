// LeetCode #1526: Minimum Number of Increments on Subarrays to Form a
// Target Array -- bench: the ★ arm over 100 random arrays of 1 to 100000 numbers up to 10000, built once and answered 50 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_number_operations(const int64_t *target, int64_t n) {
    int64_t total = target[0];
    for (int64_t i = 1; i < n; i++) {
        if (target[i] > target[i - 1]) {
            total += target[i] - target[i - 1];
        }
    }
    return total;
}

static int64_t seed = 1526;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) {
    return (check * 31 + x + 1) % 1000000007;
}

int main(void) {
    enum { COUNT = 100 };
    static int64_t *arrays[COUNT];
    static int64_t lens[COUNT];
    for (int c = 0; c < COUNT; c++) {
        int64_t hi = next_random();
        int64_t n = (hi * 32768 + next_random()) % 100000 + 1;
        arrays[c] = malloc((size_t)n * sizeof(int64_t));
        lens[c] = n;
        for (int64_t i = 0; i < n; i++) {
            hi = next_random();
            arrays[c][i] = (hi * 32768 + next_random()) % 10000 + 1;
        }
    }
    int64_t check = 0;
    for (int pass = 0; pass < 50; pass++) {
        for (int c = 0; c < COUNT; c++) {
            check = mix(check, min_number_operations(arrays[c], lens[c]));
        }
    }
    printf("50 passes over 100 arrays of up to 100000 numbers: checksum %lld\n", (long long)check);
    for (int c = 0; c < COUNT; c++) {
        free(arrays[c]);
    }
    return 0;
}
