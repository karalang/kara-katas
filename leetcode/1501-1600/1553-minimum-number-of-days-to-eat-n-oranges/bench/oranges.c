// LeetCode #1553: Minimum Number of Days to Eat N Oranges -- bench: the ★
// arm (halve or third after the single days, every answer kept in a fresh
// map per call) over 20000 piles of 1 to 2*10^9, drawn once, each asked 3
// times. C mirror of
// oranges.kara: the map is an open-addressing table of 1024 slots,
// allocated and zeroed per call, hashed by a multiply.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define CAP 1024

typedef struct { int64_t key, value; } Slot;

static int64_t days(int64_t n, Slot *memo) {
    if (n <= 1) return n;
    uint64_t h = ((uint64_t)n * 0x9E3779B97F4A7C15ull) >> 54;
    while (memo[h].key != 0) {
        if (memo[h].key == n) return memo[h].value;
        h = (h + 1) & (CAP - 1);
    }
    int64_t halve = n % 2 + days(n / 2, memo);
    int64_t third = n % 3 + days(n / 3, memo);
    int64_t best = 1 + (halve < third ? halve : third);
    h = ((uint64_t)n * 0x9E3779B97F4A7C15ull) >> 54;
    while (memo[h].key != 0) h = (h + 1) & (CAP - 1);
    memo[h].key = n;
    memo[h].value = best;
    return best;
}

static int64_t min_days(int64_t n) {
    Slot *memo = calloc(CAP, sizeof(Slot));
    int64_t d = days(n, memo);
    free(memo);
    return d;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1553;
    static int64_t piles[20000];
    for (int i = 0; i < 20000; i++) {
        int64_t wide = (next_random(&seed) * 32768 + next_random(&seed)) * 32768 + next_random(&seed);
        piles[i] = wide % 2000000000 + 1;
    }
    int64_t check = 0, total = 0;
    for (int pass = 0; pass < 3; pass++) {
        for (int i = 0; i < 20000; i++) {
            int64_t d = min_days(piles[i]);
            total += d;
            check = mix(check, d);
        }
    }
    printf("3 passes over 20000 piles of up to 2000000000: %lld days, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
