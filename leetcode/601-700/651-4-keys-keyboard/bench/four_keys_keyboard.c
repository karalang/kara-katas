// Benchmark for #651: the best for every count of presses, as the Kara
// ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_a(int64_t n) {
    int64_t *best = calloc((size_t)n + 1, sizeof *best);
    for (int64_t i = 1; i <= n; i++) {
        best[i] = best[i - 1] + 1;
        for (int64_t j = 1; j < i - 2; j++) {
            int64_t v = best[j] * (i - j - 1);
            if (v > best[i]) best[i] = v;
        }
    }
    int64_t a = best[n];
    free(best);
    return a;
}

int main(void) {
    int64_t calls = 200000, total = 0, checksum = 0;
    for (int64_t c = 0; c < calls; c++) {
        int64_t a = max_a(1 + (c * 37) % 150);
        total = (total + a) % 1000000007;
        checksum = (checksum * 31 + a % 1000000007) % 1000000007;
    }
    printf("%lld calls: total %lld, checksum %lld\n", (long long)calls,
           (long long)total, (long long)checksum);
    return 0;
}
