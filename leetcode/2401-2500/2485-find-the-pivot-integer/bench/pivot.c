// LeetCode #2485: Find the Pivot Integer -- bench, C mirror of
// pivot.kara. __builtin_sqrt of a __builtin_fabs, which the total never
// needs, and rounding by adding a half keep the link free of -lm.
#include <stdint.h>
#include <stdio.h>

static int64_t pivot_integer(int64_t n) {
    int64_t total = n * (n + 1) / 2;
    int64_t x = (int64_t)(__builtin_sqrt(__builtin_fabs((double)total)) + 0.5);
    return x * x == total ? x : -1;
}

int main(void) {
    int64_t check = 0;
    for (int64_t p = 0; p < 24000; p++) {
        int64_t start = check % 1000;
        for (int64_t i = 0; i < 1000; i++) {
            int64_t n = 1 + (start + i) % 1000;
            check = (check * 31 + pivot_integer(n) + 2 + p) % 1000000007;
        }
    }
    printf("24000 passes over every count from 1 to 1000: checksum %lld\n", (long long)check);
    return 0;
}
