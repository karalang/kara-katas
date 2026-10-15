// Benchmark for #668: binary search on the value, counting by rows, as
// the Kara ★ arm.
#include <stdint.h>
#include <stdio.h>

static int64_t find_kth_number(int64_t m, int64_t n, int64_t k) {
    int64_t lo = 1;
    int64_t hi = m * n;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        int64_t count = 0;
        for (int64_t i = 1; i <= m; i++) {
            int64_t c = mid / i;
            count += c < n ? c : n;
        }
        if (count >= k) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}

int main(void) {
    int64_t rounds = 200;
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t m = 30000 - r * 97 % 10000;
        int64_t n = 30000 - r * 89 % 10000;
        int64_t k = 1 + r * 7919813 % (m * n);
        sum = (sum * 31 + find_kth_number(m, n, k)) % 1000000007;
    }
    printf("%lld rounds: checksum %lld\n", (long long)rounds, (long long)sum);
    return 0;
}
