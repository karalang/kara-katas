// LeetCode #2088: Count Fertile Pyramids in a Land -- C mirror of the ★
// arm's benchmark (pyramids.kara): the same 20 lands, each counted 20 times
// by the same two passes, each row's heights in a `malloc`'d buffer.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define S 316

static int64_t seed = 2088;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t min3(int64_t a, int64_t b, int64_t c) {
    int64_t m = a < b ? a : b;
    return m < c ? m : c;
}

static int64_t count_one_way(int64_t (*grid)[S], const int *order, int m, int n) {
    int64_t *below = calloc(n, sizeof(int64_t));
    int64_t count = 0;
    for (int k = 0; k < m; k++) {
        int r = order[k];
        int64_t *tall = calloc(n, sizeof(int64_t));
        for (int c = 0; c < n; c++) {
            if (grid[r][c] == 0) continue;
            tall[c] = (c == 0 || c == n - 1) ? 1 : min3(below[c - 1], below[c], below[c + 1]) + 1;
            count += tall[c] - 1;
        }
        free(below);
        below = tall;
    }
    free(below);
    return count;
}

static int64_t count_pyramids(int64_t (*grid)[S]) {
    int up[S], down[S];
    for (int i = 0; i < S; i++) {
        up[i] = S - 1 - i;
        down[i] = i;
    }
    return count_one_way(grid, up, S, S) + count_one_way(grid, down, S, S);
}

int main(void) {
    int64_t (*lands)[S][S] = malloc(20 * sizeof(*lands));
    for (int t = 0; t < 20; t++) {
        int64_t odds = 15 + t % 5;
        for (int r = 0; r < S; r++)
            for (int c = 0; c < S; c++) lands[t][r][c] = next_random() % 20 < odds ? 1 : 0;
    }
    int64_t total = 0, check = 0;
    for (int round = 0; round < 20; round++) {
        for (int t = 0; t < 20; t++) {
            int64_t a = count_pyramids(lands[(t + round) % 20]);
            total += a;
            check = (check * 31 + a) % 1000000007;
        }
    }
    printf("400 counts: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    free(lands);
    return 0;
}
