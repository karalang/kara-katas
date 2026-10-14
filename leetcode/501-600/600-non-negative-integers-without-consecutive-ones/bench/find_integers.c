// Benchmark for #600: C mirror of the ★ arm (walk the bits with Fibonacci
// counts); see find_integers.kara. The counts are an array on the stack,
// filled on every call, where the Kāra arm builds a `Vec`.
#include <stdint.h>
#include <stdio.h>

static int64_t find_integers(int64_t n) {
    int64_t fib[32] = {1, 2};
    for (int k = 2; k < 32; k++) fib[k] = fib[k - 1] + fib[k - 2];
    int64_t count = 0;
    int previous = 0;
    for (int k = 31; k >= 0; k--) {
        if ((n >> k) & 1) {
            count += fib[k];
            if (previous) return count;
            previous = 1;
        } else {
            previous = 0;
        }
    }
    return count + 1;
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { COUNT = 1000000, ROUNDS = 20 };
    static int64_t values[COUNT];
    int64_t seed = 600;
    for (int i = 0; i < COUNT; i++) {
        int64_t hi = step(&seed);
        int64_t lo = step(&seed);
        values[i] = 1 + (hi * 32768 + lo) % 1000000000;
    }
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < ROUNDS; round++)
        for (int g = 0; g < COUNT; g++) {
            int64_t got = find_integers(values[((int64_t)round * 7 + g) % COUNT]);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    printf("%d values, %d rounds: total %lld, checksum %lld\n", COUNT, ROUNDS, (long long)total,
           (long long)checksum);
    return 0;
}
