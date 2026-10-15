// Benchmark for #672: the cases worked out, as the Kara ★ arm.
#include <stdint.h>
#include <stdio.h>

static int64_t flip_lights(int64_t n, int64_t m) {
    if (m == 0) {
        return 1;
    }
    if (n == 1) {
        return 2;
    }
    if (n == 2) {
        return m == 1 ? 3 : 4;
    }
    if (m == 1) {
        return 4;
    }
    if (m == 2) {
        return 7;
    }
    return 8;
}

int main(void) {
    int64_t count = 100000000;
    int64_t sum = 0;
    for (int64_t i = 0; i < count; i++) {
        sum = (sum * 31 + flip_lights(1 + i % 1000, i / 1000 % 1001)) % 1000000007;
    }
    printf("%lld queries: checksum %lld\n", (long long)count, (long long)sum);
    return 0;
}
