// LeetCode #2022: Convert 1D Array Into 2D Array -- the ★ arm in C, the same
// algorithm and workload as convert.kara: each row a fresh copy of its run.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t **construct_2d_array(const int64_t *original, int64_t len, int64_t m, int64_t n, int64_t *rows_out) {
    if (len != m * n) {
        *rows_out = 0;
        return NULL;
    }
    int64_t **grid = malloc(sizeof(int64_t *) * m);
    for (int64_t i = 0; i < m; i++) {
        grid[i] = malloc(sizeof(int64_t) * n);
        memcpy(grid[i], original + i * n, sizeof(int64_t) * n);
    }
    *rows_out = m;
    return grid;
}

static int64_t seed = 2022;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t rows_of[20] = {1, 2, 4, 5, 8, 10, 16, 20, 25, 40, 50, 80, 100, 125, 200, 250, 400, 500, 1000, 20000};
    int64_t *arrays[20];
    for (int a = 0; a < 20; a++) {
        arrays[a] = malloc(sizeof(int64_t) * 20000);
        for (int i = 0; i < 20000; i++) arrays[a][i] = next_random() % 100000 + 1;
    }
    int64_t calls = 0, rows = 0, check = 0;
    for (int r = 0; r < 200; r++) {
        for (int a = 0; a < 20; a++) {
            int64_t m = rows_of[a];
            int64_t n = a % 5 == 4 ? 20000 / m + 1 : 20000 / m;
            int64_t count;
            int64_t **grid = construct_2d_array(arrays[a], 20000, m, n, &count);
            calls++;
            if (count == 0) check = (check * 31 + 1000000006) % 1000000007;
            for (int64_t i = 0; i < count; i++) {
                rows++;
                check = (check * 31 + grid[i][0] + grid[i][n - 1]) % 1000000007;
                free(grid[i]);
            }
            free(grid);
        }
    }
    printf("%lld calls: %lld rows, checksum %lld\n", (long long)calls, (long long)rows, (long long)check);
    return 0;
}
