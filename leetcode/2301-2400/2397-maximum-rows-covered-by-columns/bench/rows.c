// LeetCode #2397: Maximum Rows Covered by Columns -- the bench, the ★ arm
// in C: each row as the mask of its 1s, every mask of numSelect columns
// tried.

#include <stdint.h>
#include <stdio.h>

static int64_t seed = 2397;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t maximum_rows(int64_t matrix[12][12], int64_t m, int64_t n, int64_t num_select) {
    int64_t masks[12];
    for (int64_t r = 0; r < m; r++) {
        int64_t mask = 0;
        for (int64_t c = 0; c < n; c++)
            if (matrix[r][c] == 1) mask |= (int64_t)1 << c;
        masks[r] = mask;
    }
    int64_t best = 0;
    for (int64_t chosen = 0; chosen < ((int64_t)1 << n); chosen++) {
        if (__builtin_popcountll((unsigned long long)chosen) != num_select) continue;
        int64_t covered = 0;
        for (int64_t r = 0; r < m; r++)
            if ((masks[r] & chosen) == masks[r]) covered++;
        if (covered > best) best = covered;
    }
    return best;
}

int main(void) {
    static int64_t grids[200][12][12];
    for (int g = 0; g < 200; g++) {
        int64_t odds = 2 + g % 4;
        for (int r = 0; r < 12; r++)
            for (int c = 0; c < 12; c++) grids[g][r][c] = next_random() % odds == 0 ? 1 : 0;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++)
        for (int g = 0; g < 200; g++)
            for (int64_t k = 1; k < 13; k++) check = (check * 31 + maximum_rows(grids[g], 12, 12, k) + p) % 1000000007;
    printf("10 passes over 200 grids of 12 by 12, every choice: checksum %lld\n", (long long)check);
    return 0;
}
