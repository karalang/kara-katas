// Benchmark for #818: Race Car -- the ★ arm (the best run to each distance).
//
// Mirrors racecar.kara: one table of the best run to every distance up to
// the target, each entry the better of overshooting and stopping short.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t racecar(int64_t target) {
    int64_t *best = calloc((size_t)(target + 1), sizeof(int64_t));
    for (int64_t t = 1; t <= target; t++) {
        int64_t n = 0;
        while (((int64_t)1 << n) <= t) n++;
        int64_t full = ((int64_t)1 << n) - 1;
        if (t == full) {
            best[t] = n;
            continue;
        }
        int64_t shortest = n + 1 + best[full - t];
        int64_t short_ = ((int64_t)1 << (n - 1)) - 1;
        for (int64_t m = 0; m < n - 1; m++) {
            int64_t back = ((int64_t)1 << m) - 1;
            int64_t steps = (n - 1) + 1 + m + 1 + best[t - short_ + back];
            if (steps < shortest) shortest = steps;
        }
        best[t] = shortest;
    }
    int64_t answer = best[target];
    free(best);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t rounds = 40000;
    int64_t seed = 818;
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t t = 1 + next_random(&seed) % 10000;
        int64_t answer = racecar(t);
        total += answer;
        checksum = (checksum * 131 + answer) % 1000000007;
    }
    printf("%lld rounds of targets up to 10000: total %lld, checksum %lld\n",
           (long long)rounds, (long long)total, (long long)checksum);
    return 0;
}
