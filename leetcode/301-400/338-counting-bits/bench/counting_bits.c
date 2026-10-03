// Benchmark workload for LeetCode #338 — C mirror of counting_bits.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define TOP_N 1000000
#define ROUNDS 300
#define MODULUS 1073741789LL

static int64_t *count_bits(int64_t n) {
    int64_t *ans = calloc((size_t)(n + 1), sizeof(int64_t));
    for (int64_t i = 1; i <= n; i++) {
        ans[i] = ans[i >> 1] + (i & 1);
    }
    return ans;
}

int main(void) {
    int64_t sink = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        int64_t n = TOP_N - r;
        int64_t *ans = count_bits(n);
        int64_t picked = ans[n] * 10000 + ans[n / 3] * 100 + ans[(n * 7) / 11];
        sink = (sink * 1000003 + picked + (n + 1)) % MODULUS;
        free(ans);
    }
    printf("%lld\n", (long long)sink);
    return 0;
}
