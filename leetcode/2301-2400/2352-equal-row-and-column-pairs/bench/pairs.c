// LeetCode #2352: Equal Row and Column Pairs -- the bench, the ★ arm in C:
// the rows counted in a hash table keyed by the row, then each column
// built and looked up there. C has no map, so the table is open
// addressing over pointers to the rows, hashed by FNV-1a over the values
// and compared in full.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 200
#define SLOTS 512

static uint64_t hash(const int64_t *values, int n) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < n; i++) {
        h ^= (uint64_t)values[i];
        h *= 1099511628211ULL;
    }
    return h;
}

static int64_t equal_pairs(int64_t grid[N][N], int n) {
    const int64_t *keys[SLOTS];
    int64_t counts[SLOTS];
    memset(keys, 0, sizeof keys);
    for (int r = 0; r < n; r++) {
        size_t s = hash(grid[r], n) & (SLOTS - 1);
        while (keys[s] && memcmp(keys[s], grid[r], n * sizeof(int64_t)) != 0) {
            s = (s + 1) & (SLOTS - 1);
        }
        if (!keys[s]) {
            keys[s] = grid[r];
            counts[s] = 0;
        }
        counts[s]++;
    }
    int64_t total = 0;
    int64_t column[N];
    for (int j = 0; j < n; j++) {
        for (int i = 0; i < n; i++) {
            column[i] = grid[i][j];
        }
        size_t s = hash(column, n) & (SLOTS - 1);
        while (keys[s] && memcmp(keys[s], column, n * sizeof(int64_t)) != 0) {
            s = (s + 1) & (SLOTS - 1);
        }
        if (keys[s]) {
            total += counts[s];
        }
    }
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // grid g is 200 x 200, cell (i, j) being (a i j + b) mod m, so that
    // rows repeat and match columns, with a in 1 to 5 and m in 2 to 10
    int64_t seed = 2352;
    int64_t (*grids)[N][N] = malloc(10 * sizeof *grids);
    for (int g = 0; g < 10; g++) {
        int64_t a = 1 + next_random(&seed) % 5;
        int64_t b = next_random(&seed) % 10;
        int64_t m = 2 + next_random(&seed) % 9;
        for (int64_t i = 0; i < N; i++) {
            for (int64_t j = 0; j < N; j++) {
                grids[g][i][j] = (a * i * j + b) % m;
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 40; p++) {
        for (int g = 0; g < 10; g++) {
            check = (check * 31 + equal_pairs(grids[g], N) + p) % 1000000007;
        }
    }
    printf("40 passes over 10 grids of 200 x 200: checksum %lld\n", (long long)check);
    free(grids);
    return 0;
}
