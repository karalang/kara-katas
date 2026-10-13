// Benchmark for #470: mirror of rand10.kara (the ★ arm: rejection
// sampling) on the same workload, over the same seeded rand7.
#include <stdint.h>
#include <stdio.h>

typedef struct {
    int64_t seed;
} Rand7;

static int64_t rand7(Rand7 *rng) {
    rng->seed = (rng->seed * 1103515245 + 12345) % 2147483648;
    return 1 + (rng->seed / 65536) % 7;
}

static int64_t rand10(Rand7 *rng) {
    for (;;) {
        int64_t a = rand7(rng);
        int64_t v = (a - 1) * 7 + rand7(rng);
        if (v <= 40) {
            return 1 + (v - 1) % 10;
        }
    }
}

int main(void) {
    const int64_t n = 20000000;
    Rand7 rng = {470};
    int64_t counts[11] = {0};
    int64_t checksum = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t value = rand10(&rng);
        counts[value] += 1;
        checksum = (checksum * 11 + value) % 1000000007;
    }
    printf("%lld draws: %lld ones, %lld tens, checksum %lld\n", (long long)n, (long long)counts[1],
           (long long)counts[10], (long long)checksum);
    return 0;
}
