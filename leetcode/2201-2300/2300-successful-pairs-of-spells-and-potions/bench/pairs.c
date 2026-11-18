// LeetCode #2300: Successful Pairs of Spells and Potions -- the bench,
// the ★ arm in C. Sort a copy of the potions with qsort, then for each
// spell binary-search the first potion whose product with it reaches
// success.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { CASES = 10, N = 100000 };

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static void successful_pairs(const int64_t *spells, int n, const int64_t *potions, int m, int64_t success,
                             int64_t *sorted, int64_t *out) {
    memcpy(sorted, potions, sizeof(int64_t) * m);
    qsort(sorted, m, sizeof(int64_t), cmp);
    for (int i = 0; i < n; i++) {
        int64_t lo = 0, hi = m;
        while (lo < hi) {
            int64_t mid = (lo + hi) / 2;
            if (spells[i] * sorted[mid] < success) lo = mid + 1;
            else hi = mid;
        }
        out[i] = m - lo;
    }
}

static int64_t seed = 2300;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t spells[CASES][N], potions[CASES][N], sorted[N], out[N];
    for (int c = 0; c < CASES; c++)
        for (int i = 0; i < N; i++) {
            int64_t hi = next_random();
            spells[c][i] = (hi * 32768 + next_random()) % 100000 + 1;
            hi = next_random();
            potions[c][i] = (hi * 32768 + next_random()) % 100000 + 1;
        }
    int64_t check = 0;
    for (int64_t p = 0; p < 5; p++)
        for (int64_t c = 0; c < CASES; c++) {
            successful_pairs(spells[c], N, potions[c], N, 1000000000LL * c + 7 + p, sorted, out);
            for (int i = 0; i < N; i++) check = (check * 31 + out[i]) % 1000000007;
        }
    printf("5 passes over 10 cases of 10^5 spells and potions: checksum %lld\n", (long long)check);
    return 0;
}
