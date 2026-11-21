// LeetCode #2507: Smallest Value After Replacing With Sum of Prime
// Factors -- C mirror of the benchmark (smallest.kara): the same passes,
// order and checksum.
#include <stdint.h>
#include <stdio.h>

static int64_t smallest_value(int64_t n) {
    for (;;) {
        int64_t rest = n, total = 0;
        for (int64_t p = 2; p * p <= rest; p++) {
            while (rest % p == 0) {
                rest /= p;
                total += p;
            }
        }
        if (rest > 1) total += rest;
        if (total == n) return n;
        n = total;
    }
}

int main(void) {
    const int64_t passes = 14;
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        int64_t start = check % 99999;
        for (int64_t k = 0; k < 99999; k++) {
            int64_t n = (start + k) % 99999 + 2;
            check = (check * 31 + smallest_value(n) + p) % 1000000007;
        }
    }
    printf("%lld passes over 2 to 10^5: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
