// Benchmark for #441: mirror of arrange_coins.kara (the closed form with
// an integer square root) on 3,000,000 random n up to 2^31 - 1.
#include <stdint.h>
#include <stdio.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

// The largest r with r * r <= x.
static int64_t isqrt(int64_t x) {
    if (x < 2) {
        return x;
    }
    int64_t r = x;
    int64_t next = (r + x / r) / 2;
    while (next < r) {
        r = next;
        next = (r + x / r) / 2;
    }
    return r;
}

static int64_t arrange_coins(int64_t n) {
    return (isqrt(8 * n + 1) - 1) / 2;
}

int main(void) {
    const int64_t count = 3000000;
    int64_t seed = 441;
    int64_t total = 0, checksum = 0;
    for (int64_t i = 0; i < count; i++) {
        int64_t a = next_random(&seed);
        int64_t high = a * 32768 + next_random(&seed);
        int64_t n = 1 + (high * 2 + next_random(&seed) % 2) % 2147483647;
        int64_t rows = arrange_coins(n);
        total += rows;
        checksum = (checksum * 31 + rows) % 1000000007;
    }
    printf("%lld random n: total %lld, checksum %lld\n", (long long)count, (long long)total, (long long)checksum);
    return 0;
}
