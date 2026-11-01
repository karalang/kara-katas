// LeetCode #1034: Coloring A Border -- bench
// Mirrors ./color_border.kara; see ../README.md § Benchmarks. Each call
// allocates its seen marks and its copy of the grid, as the Kāra and
// Rust versions do, one block each rather than one row at a time.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 50

static void visit(const int64_t *grid, int64_t m, int64_t n, int64_t r, int64_t c, int64_t color, char *seen, int64_t *out) {
    static const int64_t dirs[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    seen[r * n + c] = 1;
    int border = 0;
    for (int d = 0; d < 4; d++) {
        int64_t nr = r + dirs[d][0], nc = c + dirs[d][1];
        if (nr < 0 || nr >= m || nc < 0 || nc >= n || grid[nr * n + nc] != grid[r * n + c]) {
            border = 1;
        } else if (!seen[nr * n + nc]) {
            visit(grid, m, n, nr, nc, color, seen, out);
        }
    }
    if (border) {
        out[r * n + c] = color;
    }
}

static int64_t *color_border(const int64_t *grid, int64_t m, int64_t n, int64_t row, int64_t col, int64_t color) {
    char *seen = calloc((size_t)(m * n), 1);
    int64_t *out = malloc(sizeof(int64_t) * (size_t)(m * n));
    memcpy(out, grid, sizeof(int64_t) * (size_t)(m * n));
    visit(grid, m, n, row, col, color, seen, out);
    free(seen);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int count = 100, starts = 10, rounds = 20;
    int64_t seed = 1034;
    int64_t *grids = malloc(sizeof(int64_t) * count * N * N);
    int64_t asks[1000][4];
    int na = 0;
    for (int g = 0; g < count; g++) {
        for (int i = 0; i < N * N; i++) {
            grids[g * N * N + i] = next_random(&seed) % 3 == 0 ? 2 : 1;
        }
        for (int s = 0; s < starts; s++) {
            asks[na][0] = g;
            asks[na][1] = next_random(&seed) % 50;
            asks[na][2] = next_random(&seed) % 50;
            asks[na][3] = next_random(&seed) % 3 + 1;
            na++;
        }
    }
    int64_t changed = 0, check = 0;
    for (int round = 0; round < rounds; round++) {
        for (int a = 0; a < na; a++) {
            const int64_t *grid = grids + asks[a][0] * N * N;
            int64_t *painted = color_border(grid, N, N, asks[a][1], asks[a][2], asks[a][3]);
            for (int64_t r = 0; r < N; r++) {
                for (int64_t c = 0; c < N; c++) {
                    if (painted[r * N + c] != grid[r * N + c]) {
                        changed++;
                        check = (check * 131 + r * 50 + c) % 1000000007;
                    }
                }
            }
            free(painted);
        }
    }
    printf("%d grids of 50 by 50, %d starts each, %d rounds: %lld squares changed, checksum %lld\n", count, starts, rounds, (long long)changed, (long long)check);
    free(grids);
    return 0;
}
