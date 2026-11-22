// LeetCode #2834: Find the Minimum Possible Sum of a Beautiful Array --
// the bench, mirrored from sum.kara: two arithmetic series.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define MOD 1000000007LL

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

static int64_t minimum_possible_sum(int64_t n, int64_t target) {
    int64_t low = n < target / 2 ? n : target / 2;
    int64_t high = n - low;
    int64_t first = low * (low + 1) / 2;
    int64_t rest = high * (2 * target + high - 1) / 2;
    return (first + rest) % MOD;
}

int main(void) {
    const int64_t count = 1000000, rounds = 20;
    int64_t seed = 2834;
    int64_t *ns = malloc(sizeof(int64_t) * count), *ts = malloc(sizeof(int64_t) * count);
    for (int64_t i = 0; i < count; i++) {
        ns[i] = wide(&seed) % 1000000000 + 1;
        ts[i] = wide(&seed) % 1000000000 + 1;
    }
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++)
        for (int64_t i = 0; i < count; i++)
            check = (check * 31 + minimum_possible_sum(ns[i], ts[i]) + r) % MOD;
    printf("%lld pairs, %lld rounds: checksum %lld\n", (long long)count, (long long)rounds, (long long)check);
    free(ns); free(ts);
    return 0;
}
