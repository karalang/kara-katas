// LeetCode #2033: Minimum Operations to Make a Uni-Value Grid -- the ★ arm
// in C, the same algorithm and workload as grid.kara: the values copied
// out of the grid and sorted per call (qsort), as the Kāra program's are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define ROWS 200
#define COLS 250
#define CELLS (ROWS * COLS)

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t min_operations(int64_t grid[ROWS][COLS], int64_t x) {
    int64_t *values = malloc(CELLS * sizeof(int64_t));
    int64_t n = 0;
    for (int i = 0; i < ROWS; i++)
        for (int j = 0; j < COLS; j++)
            values[n++] = grid[i][j];
    int64_t r = values[0] % x;
    for (int64_t i = 0; i < n; i++) {
        if (values[i] % x != r) {
            free(values);
            return -1;
        }
    }
    qsort(values, n, sizeof(int64_t), cmp);
    int64_t median = values[n / 2], total = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t d = values[i] - median;
        total += (d < 0 ? -d : d) / x;
    }
    free(values);
    return total;
}

static int64_t seed = 2033;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t grids[20][ROWS][COLS];

int main(void) {
    for (int64_t a = 0; a < 20; a++) {
        int64_t x = a % 7 + 1;
        int64_t base = next_random() % x + 1;
        int64_t steps = (10000 - base) / x + 1;
        for (int i = 0; i < ROWS; i++)
            for (int j = 0; j < COLS; j++) {
                int64_t hi = next_random();
                int64_t lo = next_random();
                grids[a][i][j] = base + (hi * 32768 + lo) % steps * x;
            }
    }
    int64_t calls = 0, sum = 0, check = 0;
    for (int64_t round = 0; round < 30; round++) {
        for (int64_t a = 0; a < 20; a++) {
            int64_t x = a % 7 + 1;
            int64_t at = (round * 997 + a * 31) % CELLS;
            int64_t *cell = &grids[a][at / COLS][at % COLS];
            *cell = *cell + x <= 10000 ? *cell + x : *cell - x;
            int64_t answer = min_operations(grids[a], x);
            calls++;
            sum += answer;
            check = (check * 31 + answer) % 1000000007LL;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
