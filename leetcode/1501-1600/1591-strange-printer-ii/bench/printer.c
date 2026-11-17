// LeetCode #1591: Strange Printer II -- the bench in C, mirroring
// printer.kara. Each grid row is its own malloc, as each Kāra row is a
// `Vec`; the 61 by 61 order matrix and the counts are allocated per call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int is_printable(int32_t **grid, int64_t rows, int64_t cols) {
    int64_t top[61], bottom[61], left[61], right[61], before[61];
    for (int k = 0; k < 61; k++) {
        top[k] = rows;
        bottom[k] = -1;
        left[k] = cols;
        right[k] = -1;
        before[k] = 0;
    }
    for (int64_t r = 0; r < rows; r++)
        for (int64_t c = 0; c < cols; c++) {
            int k = grid[r][c];
            if (r < top[k]) top[k] = r;
            if (r > bottom[k]) bottom[k] = r;
            if (c < left[k]) left[k] = c;
            if (c > right[k]) right[k] = c;
        }
    uint8_t *after = calloc(61 * 61, 1);
    for (int k = 1; k < 61; k++)
        for (int64_t r = top[k]; r < bottom[k] + 1; r++)
            for (int64_t c = left[k]; c < right[k] + 1; c++) {
                int other = grid[r][c];
                if (other != k && !after[k * 61 + other]) {
                    after[k * 61 + other] = 1;
                    before[other] += 1;
                }
            }
    int ready[61];
    int n = 0;
    for (int k = 1; k < 61; k++)
        if (before[k] == 0) ready[n++] = k;
    int taken = 0;
    while (n > 0) {
        int k = ready[--n];
        taken++;
        for (int other = 1; other < 61; other++)
            if (after[k * 61 + other]) {
                if (--before[other] == 0) ready[n++] = other;
            }
    }
    free(after);
    return taken == 60;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define MAX(a, b) ((a) > (b) ? (a) : (b))

int main(void) {
    int64_t seed = 1591;
    int32_t ***grids = malloc(4000 * sizeof(int32_t **));
    for (int g = 0; g < 4000; g++) {
        int32_t order[60];
        for (int i = 0; i < 60; i++) order[i] = i + 1;
        for (int i = 59; i >= 1; i--) {
            int j = (int)(next_random(&seed) % (i + 1));
            int32_t t = order[i];
            order[i] = order[j];
            order[j] = t;
        }
        int32_t **grid = malloc(60 * sizeof(int32_t *));
        for (int r = 0; r < 60; r++) {
            grid[r] = malloc(60 * sizeof(int32_t));
            for (int c = 0; c < 60; c++) grid[r][c] = order[0];
        }
        for (int i = 1; i < 60; i++) {
            int64_t r1 = next_random(&seed) % 60, r2 = next_random(&seed) % 60;
            int64_t c1 = next_random(&seed) % 60, c2 = next_random(&seed) % 60;
            for (int64_t r = MIN(r1, r2); r <= MAX(r1, r2); r++)
                for (int64_t c = MIN(c1, c2); c <= MAX(c1, c2); c++) grid[r][c] = order[i];
        }
        if (g % 2 == 1) {
            int64_t r = next_random(&seed) % 60;
            int64_t c = next_random(&seed) % 60;
            grid[r][c] = (int32_t)(next_random(&seed) % 60 + 1);
        }
        grids[g] = grid;
    }
    int64_t check = 0;
    int yes = 0;
    for (int g = 0; g < 4000; g++) {
        int ok = is_printable(grids[g], 60, 60);
        yes += ok;
        check = (check * 31 + ok + 1) % 1000000007;
    }
    printf("4000 grids of 60 by 60: %d printable, checksum %lld\n", yes, (long long)check);
    return 0;
}
