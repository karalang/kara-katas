// Benchmark for #849: Maximize Distance to Closest Person -- C twin of the
// Kāra ★ arm (one pass, remembering the last person).
#include <stdio.h>
#include <stdint.h>

#define N 20000

static int64_t max_dist_to_closest(const int64_t *seats, int64_t n) {
    int64_t last = -1, best = 0;
    for (int64_t i = 0; i < n; i++) {
        if (seats[i] == 1) {
            if (last < 0) best = i;
            else if ((i - last) / 2 > best) best = (i - last) / 2;
            last = i;
        }
    }
    return n - 1 - last > best ? n - 1 - last : best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 20000, n = N;
    int64_t seed = 849;
    static int64_t rows[64][N];
    for (int64_t g = 0; g < count; g++) {
        int64_t odds = 2LL << (g % 8);
        for (int64_t i = 0; i < n; i++) rows[g][i] = next_random(&seed) % odds == 0 ? 1 : 0;
        int64_t taken = next_random(&seed) % n;
        int64_t empty = (taken + 1 + next_random(&seed) % (n - 1)) % n;
        rows[g][taken] = 1;
        rows[g][empty] = 0;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t d = max_dist_to_closest(rows[round % count], n);
        total += d;
        checksum = (checksum * 31 + d) % 1000000007;
    }
    printf("%lld rounds of %lld rows: distances sum to %lld, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    return 0;
}
