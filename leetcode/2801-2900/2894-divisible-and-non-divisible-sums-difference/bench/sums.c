// LeetCode #2894: Divisible and Non-divisible Sums Difference -- the
// bench, as sums.kara: every n and m from 1 to 1000, 100 rounds, by the
// formula arm.

#include <stdint.h>
#include <stdio.h>

static int64_t difference_of_sums(int64_t n, int64_t m) {
    int64_t k = n / m;
    return n * (n + 1) / 2 - m * k * (k + 1);
}

int main(void) {
    const int64_t rounds = 100, top = 1000;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t n = 1; n <= top; n++) {
            for (int64_t m = 1; m <= top; m++) {
                int64_t d = difference_of_sums(n, (m + r) % top + 1);
                total += d;
                check = (check * 31 + d + 1000000) % 1000000007;
            }
        }
    }
    printf("%lld by %lld pairs, %lld rounds: differences total %lld, checksum %lld\n", (long long)top, (long long)top,
           (long long)rounds, (long long)total, (long long)check);
    return 0;
}
