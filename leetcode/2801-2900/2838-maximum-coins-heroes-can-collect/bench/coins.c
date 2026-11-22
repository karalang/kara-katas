// LeetCode #2838: Maximum Coins Heroes Can Collect -- the bench, mirrored
// from coins.kara: sorted monsters, prefix sums, a binary search a hero.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct { int64_t power, coins; } Pair;

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

static int cmp(const void *a, const void *b) {
    const Pair *x = a, *y = b;
    if (x->power != y->power) return x->power < y->power ? -1 : 1;
    return (x->coins > y->coins) - (x->coins < y->coins);
}

static void maximum_coins(const int64_t *heroes, int64_t n, const int64_t *monsters, const int64_t *coins,
                          int64_t m, int64_t *out) {
    Pair *pairs = malloc(sizeof(Pair) * m);
    for (int64_t j = 0; j < m; j++) pairs[j] = (Pair){monsters[j], coins[j]};
    qsort(pairs, m, sizeof(Pair), cmp);
    int64_t *prefix = malloc(sizeof(int64_t) * (m + 1));
    prefix[0] = 0;
    for (int64_t j = 0; j < m; j++) prefix[j + 1] = prefix[j] + pairs[j].coins;
    for (int64_t i = 0; i < n; i++) {
        int64_t lo = 0, hi = m;
        while (lo < hi) {
            int64_t mid = lo + (hi - lo) / 2;
            if (pairs[mid].power <= heroes[i]) lo = mid + 1; else hi = mid;
        }
        out[i] = prefix[lo];
    }
    free(pairs); free(prefix);
}

int main(void) {
    const int64_t count = 10, rounds = 5, n = 100000;
    int64_t seed = 2838;
    int64_t *heroes = malloc(sizeof(int64_t) * count * n), *monsters = malloc(sizeof(int64_t) * count * n),
            *coins = malloc(sizeof(int64_t) * count * n), *out = malloc(sizeof(int64_t) * n);
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < n; i++) heroes[c * n + i] = wide(&seed) % 1000000000 + 1;
        for (int64_t i = 0; i < n; i++) monsters[c * n + i] = wide(&seed) % 1000000000 + 1;
        for (int64_t i = 0; i < n; i++) coins[c * n + i] = wide(&seed) % 1000000000 + 1;
    }
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            maximum_coins(heroes + c * n, n, monsters + c * n, coins + c * n, n, out);
            for (int64_t i = 0; i < n; i++) check = (check * 31 + out[i] % 1000000007 + r) % 1000000007;
        }
    }
    printf("%lld battles of %lld, %lld rounds: checksum %lld\n", (long long)count, (long long)n, (long long)rounds, (long long)check);
    free(heroes); free(monsters); free(coins); free(out);
    return 0;
}
