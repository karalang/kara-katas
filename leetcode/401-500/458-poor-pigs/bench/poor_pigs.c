// Benchmark for #458: mirror of poor_pigs.kara (the ★ arm, growing the
// number of outcomes) on the same workload.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t poor_pigs(int64_t buckets, int64_t minutes_to_die, int64_t minutes_to_test) {
    int64_t states = minutes_to_test / minutes_to_die + 1;
    int64_t pigs = 0;
    int64_t covered = 1;
    while (covered < buckets) {
        covered *= states;
        pigs += 1;
    }
    return pigs;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t n = 1000000;
    const int64_t rounds = 20;
    int64_t seed = 458;
    int64_t *buckets = malloc(n * sizeof(int64_t));
    int64_t *die = malloc(n * sizeof(int64_t));
    int64_t *test = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        int64_t digits = next_random(&seed) % 13;
        int64_t top = 1;
        for (int64_t j = 0; j < digits; j++) {
            top *= 10;
        }
        int64_t a = next_random(&seed);
        int64_t b = next_random(&seed);
        int64_t c = next_random(&seed);
        int64_t r = (a * 65536 + b) * 65536 + c;
        buckets[i] = 1 + r % top;
        int64_t d = 1 + next_random(&seed) % 100;
        die[i] = d;
        test[i] = d + next_random(&seed) % (101 - d);
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t hi = next_random(&seed);
        int64_t lo = next_random(&seed);
        int64_t k = (hi * 65536 + lo) % n;
        hi = next_random(&seed);
        lo = next_random(&seed);
        buckets[k] = 1 + (hi * 65536 + lo) % 1000000000000LL;
        int64_t sum = 0;
        for (int64_t i = 0; i < n; i++) {
            sum += poor_pigs(buckets[i], die[i], test[i]);
        }
        total += sum;
        checksum = (checksum * 31 + sum) % 1000000007;
    }
    printf("%lld rounds on %lld queries: %lld pigs, checksum %lld\n", (long long)rounds,
           (long long)n, (long long)total, (long long)checksum);
    free(buckets);
    free(die);
    free(test);
    return 0;
}
