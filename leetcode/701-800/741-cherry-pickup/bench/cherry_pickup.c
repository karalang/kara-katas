// LeetCode #741: Cherry Pickup -- two walkers, one layer at a time.
// Benchmark mirror of the Kara star arm: two walkers go from the near
// corner to the far one together, a cherry on a shared cell counted
// once; keep the best cherries for every pair of rows after k steps
// and build the next layer from it. Each layer is a fresh table of
// rows allocated one by one, as in the Kara arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t **new_layer(int64_t n) {
    int64_t **t = malloc(n * sizeof(int64_t *));
    for (int64_t r = 0; r < n; r++) {
        t[r] = malloc(n * sizeof(int64_t));
        for (int64_t c = 0; c < n; c++) t[r][c] = -1;
    }
    return t;
}

static void free_layer(int64_t **t, int64_t n) {
    for (int64_t r = 0; r < n; r++) free(t[r]);
    free(t);
}

static int64_t cherry_pickup(int64_t **grid, int64_t n) {
    int64_t **best = new_layer(n);
    if (grid[0][0] == -1) {
        free_layer(best, n);
        return 0;
    }
    best[0][0] = grid[0][0];
    for (int64_t k = 1; k < 2 * n - 1; k++) {
        int64_t **next = new_layer(n);
        int64_t low = k >= n ? k - n + 1 : 0;
        int64_t high = k < n ? k : n - 1;
        for (int64_t r1 = low; r1 <= high; r1++) {
            for (int64_t r2 = low; r2 <= high; r2++) {
                int64_t c1 = k - r1, c2 = k - r2;
                if (grid[r1][c1] == -1 || grid[r2][c2] == -1) continue;
                int64_t from = -1;
                for (int64_t d1 = 0; d1 < 2; d1++)
                    for (int64_t d2 = 0; d2 < 2; d2++) {
                        int64_t p1 = r1 - d1, p2 = r2 - d2;
                        if (p1 >= 0 && p2 >= 0 && best[p1][p2] > from) from = best[p1][p2];
                    }
                if (from == -1) continue;
                int64_t here = grid[r1][c1];
                if (r2 != r1) here += grid[r2][c2];
                next[r1][r2] = from + here;
            }
        }
        free_layer(best, n);
        best = next;
    }
    int64_t last = best[n - 1][n - 1];
    free_layer(best, n);
    return last == -1 ? 0 : last;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 741, n = 50, total = 0;
    int64_t **grid = malloc(n * sizeof(int64_t *));
    for (int64_t r = 0; r < n; r++) {
        grid[r] = malloc(n * sizeof(int64_t));
        for (int64_t c = 0; c < n; c++) {
            int corner = (r == 0 && c == 0) || (r == n - 1 && c == n - 1);
            if (!corner && next_random(&seed) % 10 == 0)
                grid[r][c] = -1;
            else
                grid[r][c] = next_random(&seed) % 2;
        }
    }
    for (int round = 0; round < 300; round++) {
        for (int k = 0; k < 5; k++) {
            int64_t r = next_random(&seed) % n;
            int64_t c = next_random(&seed) % n;
            int64_t v = next_random(&seed) % 10;
            int corner = (r == 0 && c == 0) || (r == n - 1 && c == n - 1);
            if (!corner) grid[r][c] = v == 0 ? -1 : v % 2;
        }
        total += cherry_pickup(grid, n);
    }
    printf("300 rounds of a 50 by 50 grid: %lld cherries in all\n", (long long)total);
    return 0;
}
