// LeetCode #1020: Number of Enclaves -- bench
// Mirrors ./enclaves.kara; see ../README.md § Benchmarks.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t i, j;
} Cell;

static int64_t num_enclaves(int64_t **grid, int64_t m, int64_t n) {
    int64_t **land = malloc(m * sizeof *land);
    for (int64_t i = 0; i < m; i++) {
        land[i] = malloc(n * sizeof **land);
        memcpy(land[i], grid[i], n * sizeof **land);
    }
    int64_t cap = 16, len = 0;
    Cell *stack = malloc(cap * sizeof *stack);
    for (int64_t i = 0; i < m; i++) {
        for (int64_t j = 0; j < n; j++) {
            if ((i == 0 || j == 0 || i == m - 1 || j == n - 1) && land[i][j] == 1) {
                land[i][j] = 0;
                if (len == cap) stack = realloc(stack, (cap *= 2) * sizeof *stack);
                stack[len++] = (Cell){i, j};
            }
        }
    }
    static const int64_t steps[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    while (len > 0) {
        Cell c = stack[--len];
        for (int s = 0; s < 4; s++) {
            int64_t a = c.i + steps[s][0], b = c.j + steps[s][1];
            if (a >= 0 && a < m && b >= 0 && b < n && land[a][b] == 1) {
                land[a][b] = 0;
                if (len == cap) stack = realloc(stack, (cap *= 2) * sizeof *stack);
                stack[len++] = (Cell){a, b};
            }
        }
    }
    int64_t left = 0;
    for (int64_t i = 0; i < m; i++) {
        for (int64_t j = 0; j < n; j++) left += land[i][j];
        free(land[i]);
    }
    free(land);
    free(stack);
    return left;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 100, rounds = 20;
    int64_t seed = 1020, cells = 0;
    int64_t ***grids = malloc(count * sizeof *grids);
    int64_t *ms = malloc(count * sizeof *ms), *ns = malloc(count * sizeof *ns);
    for (int64_t g = 0; g < count; g++) {
        int64_t m = next_random(&seed) % 500 + 1;
        int64_t n = next_random(&seed) % 500 + 1;
        int64_t land = 2 + next_random(&seed) % 5;
        grids[g] = malloc(m * sizeof *grids[g]);
        for (int64_t i = 0; i < m; i++) {
            grids[g][i] = malloc(n * sizeof **grids[g]);
            for (int64_t j = 0; j < n; j++) grids[g][i][j] = next_random(&seed) % 8 < land ? 1 : 0;
        }
        ms[g] = m;
        ns[g] = n;
        cells += m * n;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t a = num_enclaves(grids[g], ms[g], ns[g]);
            total += a;
            check = (check * 31 + a) % 1000000007;
        }
    }
    printf("%lld grids, %lld cells, %lld rounds: %lld enclaves, checksum %lld\n", (long long)count,
           (long long)cells, (long long)rounds, (long long)total, (long long)check);
    return 0;
}
