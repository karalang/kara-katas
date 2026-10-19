// Benchmark for #779: K-th Symbol in Grammar -- mirror of the ★ arm (the
// ones in k - 1), with the same workload as the Kāra program.
#include <stdint.h>
#include <stdio.h>

static int64_t kth_grammar(int64_t n, int64_t k) {
    (void)n;
    return __builtin_popcountll((uint64_t)(k - 1)) % 2;
}

int main(void) {
    int64_t x = 779, ones = 0;
    for (int64_t i = 0; i < 200000000; i++) {
        int64_t k = 1 + x % 536870912;
        int64_t answer = kth_grammar(30, k);
        ones += answer;
        x = (x * 1103515245 + 12345 + answer) % 2147483648;
    }
    printf("200000000 queries of row 30: %lld ones, last state %lld\n", (long long)ones, (long long)x);
    return 0;
}
