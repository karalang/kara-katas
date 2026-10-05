// Benchmark workload for LeetCode #343 — C mirror of integer_break.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LEN 20000
#define PUNCHES 20
#define MODULUS 1073741789LL

static int64_t integer_break(int64_t n) {
    int64_t *best = calloc((size_t)(n + 1), sizeof(int64_t));
    for (int64_t i = 2; i <= n; i++) {
        for (int64_t j = 1; j < i; j++) {
            int64_t whole = j * (i - j);
            int64_t broken = j * best[i - j];
            if (whole > best[i]) {
                best[i] = whole;
            }
            if (broken > best[i]) {
                best[i] = broken;
            }
        }
    }
    int64_t r = best[n];
    free(best);
    return r;
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 343;
    int64_t *a = malloc(sizeof(int64_t) * LEN);
    for (int64_t i = 0; i < LEN; i++) {
        a[i] = 2 + next(&seed) % 57;
    }
    int64_t sink = 0;
    for (int64_t p = 0; p < PUNCHES; p++) {
        /* Two draws, in order: C leaves the order of `next(seed) * 32768 +
           next(seed)` unspecified, so name them. */
        int64_t x = next(&seed);
        int64_t y = next(&seed);
        int64_t pos = (x * 32768 + y) % LEN;
        a[pos] = 2 + next(&seed) % 57;
        int64_t sum = 0;
        for (int64_t i = 0; i < LEN; i++) {
            sum = (sum + integer_break(a[i])) % MODULUS;
        }
        sink = (sink * 31 + sum) % MODULUS;
    }
    printf("sink %lld\n", (long long)sink);
    free(a);
    return 0;
}
