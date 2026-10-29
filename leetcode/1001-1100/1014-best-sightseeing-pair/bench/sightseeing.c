// LeetCode #1014: Best Sightseeing Pair -- bench
// Mirrors sightseeing.kara; see ../README.md § Benchmarks.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_score_sightseeing_pair(const int64_t *values, int64_t n) {
    int64_t best_first = values[0];
    int64_t best = 0;
    for (int64_t j = 1; j < n; j++) {
        int64_t score = best_first + values[j] - j;
        if (score > best) {
            best = score;
        }
        if (values[j] + j > best_first) {
            best_first = values[j] + j;
        }
    }
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t count = 50000;
    int64_t rounds = 10000;
    int64_t seed = 1014;
    int64_t *values = malloc(count * sizeof(int64_t));
    for (int64_t i = 0; i < count; i++) {
        values[i] = 1 + next_random(&seed) % 1000;
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t hi = next_random(&seed);
        int64_t lo = next_random(&seed);
        int64_t at = (hi * 32768 + lo) % count;
        values[at] = 1 + next_random(&seed) % 1000;
        int64_t answer = max_score_sightseeing_pair(values, count);
        total += answer;
        check = (check * 31 + answer) % 1000000007;
    }
    printf("%lld rounds over %lld values: answers sum to %lld, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)check);
    free(values);
    return 0;
}
