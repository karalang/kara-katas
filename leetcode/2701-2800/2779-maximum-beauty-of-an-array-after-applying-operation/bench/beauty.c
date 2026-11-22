// LeetCode #2779: Maximum Beauty of an Array After Applying Operation --
// the bench in C: the ★ arm over 20 arrays of 10^5 numbers, all drawn
// first, then each answered 10 times, every answer sorting its own copy
// by `qsort`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 20
#define N 100000

static int64_t seed = 2779;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t sorted[N];

static int64_t maximum_beauty(const int64_t *nums, int64_t n, int64_t k) {
    memcpy(sorted, nums, sizeof(int64_t) * n);
    qsort(sorted, n, sizeof(int64_t), cmp);
    int64_t best = 0, lo = 0;
    for (int64_t hi = 0; hi < n; hi++) {
        while (sorted[hi] - sorted[lo] > 2 * k) lo++;
        if (hi - lo + 1 > best) best = hi - lo + 1;
    }
    return best;
}

static int64_t cases[COUNT][N], ks[COUNT];

int main(void) {
    int rounds = 10;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) cases[c][i] = wide() % 100001;
        ks[c] = wide() % 1001;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t b = maximum_beauty(cases[c], N, ks[c]);
            total += b;
            check = (check * 31 + b + r) % 1000000007;
        }
    }
    printf("%d arrays of 10^5, %d rounds: beauties sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
