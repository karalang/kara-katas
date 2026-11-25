// LeetCode #1388 bench -- C: the ★ arm: the better of two straight runs,
// without the last slice and without the first; in each, best[i][j] is
// the most from at most j slices, no two adjacent, among the first i.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LEN 498

static int slices[LEN];

static int best_in_line(const int *s, int len, int n) {
    int *best = calloc((size_t)(len + 1) * (n + 1), sizeof(int));
    for (int i = 1; i <= len; i++) {
        for (int j = 1; j <= n; j++) {
            int skip = best[(i - 1) * (n + 1) + j];
            int take = (i >= 2 ? best[(i - 2) * (n + 1) + j - 1] : 0) + s[i - 1];
            best[i * (n + 1) + j] = skip > take ? skip : take;
        }
    }
    int out = best[len * (n + 1) + n];
    free(best);
    return out;
}

static int max_size_slices(void) {
    int n = LEN / 3;
    int a = best_in_line(slices, LEN - 1, n), b = best_in_line(slices + 1, LEN - 1, n);
    return a > b ? a : b;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1388;
    for (int i = 0; i < LEN; i++) slices[i] = (int)(1 + next_random(&seed) % 1000);
    int64_t check = 0;
    for (int round = 0; round < 1000; round++) {
        seed = (seed + check) % 2147483648LL;
        int at = (int)(next_random(&seed) % LEN);
        slices[at] = (int)(1 + next_random(&seed) % 1000);
        check = (check * 131 + max_size_slices()) % 1000000007;
    }
    printf("1000 rounds over 498 slices: checksum %lld\n", (long long)check);
    return 0;
}
