// Benchmark workload for LeetCode #335 — C mirror of self_crossing.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOVES 1000000LL
#define PUNCHES 100
#define MODULUS 1073741789LL

static int is_self_crossing(const int64_t *d, int64_t n) {
    for (int64_t i = 3; i < n; i++) {
        if (d[i] >= d[i - 2] && d[i - 1] <= d[i - 3]) return 1;
        if (i >= 4 && d[i - 1] == d[i - 3] && d[i] + d[i - 4] >= d[i - 2]) return 1;
        if (i >= 5 && d[i - 2] >= d[i - 4] && d[i] + d[i - 4] >= d[i - 2] &&
            d[i - 1] <= d[i - 3] && d[i - 1] + d[i - 5] >= d[i - 3])
            return 1;
    }
    return 0;
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t hi = next(seed);
    return hi * 32768 + next(seed);
}

int main(void) {
    int64_t *d = malloc(sizeof(int64_t) * MOVES);
    int64_t seed = 335;
    for (int64_t i = 0; i < MOVES; i++) {
        int64_t two_back = i >= 2 ? d[i - 2] : 0;
        d[i] = two_back + 1 + next(&seed) % 3;
    }
    int64_t sink = 0;
    for (int64_t p = 0; p < PUNCHES; p++) {
        int64_t at = 2 + wide(&seed) % (MOVES - 2);
        int64_t old = d[at];
        if (p % 2 == 0) d[at] = 1;
        int64_t answer = is_self_crossing(d, MOVES);
        d[at] = old;
        sink = (sink * 1000003 + answer * 2000003 + at) % MODULUS;
    }
    printf("%lld\n", (long long)sink);
    free(d);
    return 0;
}
