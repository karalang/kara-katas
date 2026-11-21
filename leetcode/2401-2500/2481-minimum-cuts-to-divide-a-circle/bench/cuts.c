// LeetCode #2481: Minimum Cuts to Divide a Circle -- bench, C mirror of
// cuts.kara.
#include <stdint.h>
#include <stdio.h>

static int64_t number_of_cuts(int64_t n) {
    if (n == 1) return 0;
    if (n % 2 == 0) return n / 2;
    return n;
}

int main(void) {
    int64_t check = 0;
    for (int64_t p = 0; p < 500000; p++) {
        int64_t start = check % 100;
        for (int64_t i = 0; i < 100; i++) {
            int64_t n = 1 + (start + i) % 100;
            check = (check * 31 + number_of_cuts(n) + p) % 1000000007;
        }
    }
    printf("500000 passes over every count from 1 to 100: checksum %lld\n", (long long)check);
    return 0;
}
