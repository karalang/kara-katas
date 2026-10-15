// Benchmark for #667: zigzag from both ends, as the Kara ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *construct_array(int64_t n, int64_t k) {
    int64_t *out = malloc(n * sizeof(int64_t));
    int64_t len = 0;
    int64_t lo = 1, hi = k + 1;
    while (lo <= hi) {
        out[len++] = lo++;
        if (lo <= hi) {
            out[len++] = hi--;
        }
    }
    for (int64_t x = k + 2; x <= n; x++) {
        out[len++] = x;
    }
    return out;
}

int main(void) {
    int64_t n = 10000;
    int64_t rounds = 10000;
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t k = 1 + r * 7919 % (n - 1);
        int64_t *a = construct_array(n, k);
        for (int64_t i = 0; i < n; i++) {
            sum = (sum * 31 + a[i]) % 1000000007;
        }
        free(a);
    }
    printf("n = %lld, %lld rounds: checksum %lld\n", (long long)n, (long long)rounds, (long long)sum);
    return 0;
}
