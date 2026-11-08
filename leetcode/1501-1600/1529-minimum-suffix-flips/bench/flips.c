// LeetCode #1529: Minimum Suffix Flips -- bench: the ★ arm over 200
// random strings of 1 to 100000 bits, built once and answered 50 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_flips(const char *target, int64_t n) {
    int64_t flips = 0;
    char prev = '0';
    for (int64_t i = 0; i < n; i++) {
        if (target[i] != prev) {
            flips++;
            prev = target[i];
        }
    }
    return flips;
}

static int64_t seed = 1529;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) {
    return (check * 31 + x + 1) % 1000000007;
}

int main(void) {
    enum { COUNT = 200 };
    static char *targets[COUNT];
    static int64_t lens[COUNT];
    for (int c = 0; c < COUNT; c++) {
        int64_t hi = next_random();
        int64_t n = (hi * 32768 + next_random()) % 100000 + 1;
        int64_t ones = next_random() % 9 + 1;
        targets[c] = malloc((size_t)n + 1);
        lens[c] = n;
        for (int64_t i = 0; i < n; i++) {
            targets[c][i] = next_random() % 10 < ones ? '1' : '0';
        }
        targets[c][n] = 0;
    }
    int64_t check = 0;
    for (int pass = 0; pass < 50; pass++) {
        for (int c = 0; c < COUNT; c++) {
            check = mix(check, min_flips(targets[c], lens[c]));
        }
    }
    printf("50 passes over 200 strings of up to 100000 bits: checksum %lld\n", (long long)check);
    for (int c = 0; c < COUNT; c++) {
        free(targets[c]);
    }
    return 0;
}
