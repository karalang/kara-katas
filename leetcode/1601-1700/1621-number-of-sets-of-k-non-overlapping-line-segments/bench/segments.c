// LeetCode #1621: Number of Sets of K Non-Overlapping Line Segments -- the
// bench in C, mirroring segments.kara: C(n + k - 1, 2k) by factorials and
// Fermat's inverse, the factorials made afresh for every query.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static int64_t power(int64_t base, int64_t exp) {
    int64_t result = 1, b = base % MOD, e = exp;
    while (e > 0) {
        if (e & 1) result = result * b % MOD;
        b = b * b % MOD;
        e >>= 1;
    }
    return result;
}

static int32_t number_of_sets(int32_t n, int32_t k) {
    int64_t top = (int64_t)n + k - 1;
    int64_t pick = 2 * (int64_t)k;
    int64_t *fact = malloc(sizeof(int64_t) * (size_t)(top + 1));
    fact[0] = 1;
    for (int64_t i = 1; i <= top; i++) fact[i] = fact[i - 1] * i % MOD;
    int64_t below = fact[pick] * fact[top - pick] % MOD;
    int32_t ways = (int32_t)(fact[top] * power(below, MOD - 2) % MOD);
    free(fact);
    return ways;
}

static int64_t seed = 1621;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 400000 };
    int32_t *ns = malloc(sizeof(int32_t) * COUNT), *ks = malloc(sizeof(int32_t) * COUNT);
    for (int i = 0; i < COUNT; i++) {
        ns[i] = (int32_t)(next_random() % 999 + 2);
        ks[i] = (int32_t)(next_random() % (ns[i] - 1) + 1);
    }
    int64_t check = 0, total = 0;
    for (int i = 0; i < COUNT; i++) {
        int32_t ways = number_of_sets(ns[i], ks[i]);
        total = (total + ways) % MOD;
        check = (check * 31 + ways + 1) % 1000000007;
    }
    printf("400000 random pairs: counts sum to %lld mod 10^9 + 7, checksum %lld\n", (long long)total,
           (long long)check);
    free(ns);
    free(ks);
    return 0;
}
