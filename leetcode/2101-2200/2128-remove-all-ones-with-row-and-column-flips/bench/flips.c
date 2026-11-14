// LeetCode #2128: Remove All Ones With Row and Column Flips -- the
// benchmark, the same algorithm as flips.kara; each grid one block of
// rows.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 300

static int64_t seed = 2128;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int remove_ones(const int64_t *grid) {
    const int64_t *first = grid;
    for (int i = 0; i < N; i++) {
        const int64_t *row = grid + i * N;
        for (int j = 0; j < N; j++) {
            if ((row[j] ^ row[0]) != (first[j] ^ first[0])) return 0;
        }
    }
    return 1;
}

int main(void) {
    int64_t *grids = malloc(sizeof(int64_t) * 20 * N * N);
    int64_t columns[N];
    for (int k = 0; k < 20; k++) {
        for (int j = 0; j < N; j++) columns[j] = next_random() % 2;
        for (int i = 0; i < N; i++) {
            int64_t r = next_random() % 2;
            for (int j = 0; j < N; j++) grids[(int64_t)k * N * N + i * N + j] = columns[j] ^ r;
        }
    }
    int64_t cleared = 0, check = 0;
    for (int64_t round = 0; round < 100; round++) {
        for (int64_t k = 0; k < 20; k++) {
            int64_t *grid = grids + k * N * N;
            int64_t r = next_random() % N;
            for (int j = 0; j < N; j++) grid[r * N + j] = 1 - grid[r * N + j];
            int broken = next_random() % 2 == 0;
            int64_t i = next_random() % N;
            int64_t j = next_random() % N;
            if (broken) grid[i * N + j] = 1 - grid[i * N + j];
            if (remove_ones(grid)) {
                cleared++;
                check = (check * 31 + round * 20 + k) % 1000000007;
            }
            if (broken) grid[i * N + j] = 1 - grid[i * N + j];
        }
    }
    printf("2000 solves: %lld cleared, checksum %lld\n", (long long)cleared, (long long)check);
    free(grids);
    return 0;
}
