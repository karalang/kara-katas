// LeetCode #875 bench: C mirror of min_eating_speed.kara (the ★ arm,
// binary search on the speed) on the same 600 searches.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t hours(const int64_t *piles, int n, int64_t k) {
    int64_t total = 0;
    for (int i = 0; i < n; i++) {
        total += (piles[i] + k - 1) / k;
    }
    return total;
}

static int64_t min_eating_speed(const int64_t *piles, int n, int64_t h) {
    int64_t lo = 1, hi = 1;
    for (int i = 0; i < n; i++) {
        if (piles[i] > hi) hi = piles[i];
    }
    while (lo < hi) {
        int64_t k = (lo + hi) / 2;
        if (hours(piles, n, k) <= h) {
            hi = k;
        } else {
            lo = k + 1;
        }
    }
    return lo;
}

static int64_t seed = 875;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t up_to(int64_t limit) {
    int64_t a = next_random();
    int64_t b = next_random();
    return (a * 32768 + b) % limit + 1;
}

int main(void) {
    enum { SETS = 20, N = 10000 };
    int64_t *pile_sets = malloc(sizeof(int64_t) * SETS * N);
    for (int k = 0; k < SETS; k++) {
        int64_t limit = k % 2 == 0 ? 1000000000 : 1000000;
        for (int i = 0; i < N; i++) {
            pile_sets[k * N + i] = up_to(limit);
        }
    }
    int64_t total = 0, check = 0;
    for (int k = 0; k < 600; k++) {
        int64_t h = 10000 + up_to(k % 3 == 0 ? 1000000000 - 10000 : 1000000) - 1;
        int64_t answer = min_eating_speed(pile_sets + (k % SETS) * N, N, h);
        total += answer;
        check = (check * 131 + answer) % 1000000007;
    }
    printf("600 searches over 10000 piles: speeds sum to %lld, checksum %lld\n",
           (long long)total, (long long)check);
    free(pile_sets);
    return 0;
}
