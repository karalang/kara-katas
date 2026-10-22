// LeetCode #861: Score After Flipping Matrix -- C mirror of the bench
// program (the ★ arm, count each column against the first).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t matrix_score(int64_t **grid, int64_t m, int64_t n) {
    int64_t score = 0;
    for (int64_t j = 0; j < n; j++) {
        int64_t ones = 0;
        for (int64_t i = 0; i < m; i++) {
            if (grid[i][j] == grid[i][0]) {
                ones++;
            }
        }
        score = score * 2 + (ones > m - ones ? ones : m - ones);
    }
    return score;
}

static int64_t seed = 861;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t size = 20;
    int64_t rounds = 1000000;
    int64_t **grid = malloc(size * sizeof(int64_t *));
    for (int64_t i = 0; i < size; i++) {
        grid[i] = malloc(size * sizeof(int64_t));
        for (int64_t j = 0; j < size; j++) {
            grid[i][j] = next_random() % 2;
        }
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t cell = next_random() % (size * size);
        int64_t i = cell / size;
        int64_t j = cell % size;
        grid[i][j] = 1 - grid[i][j];
        int64_t s = matrix_score(grid, size, size);
        grid[i][j] = 1 - grid[i][j];
        total += s;
        check = (check * 31 + s) % 1000000007;
    }
    printf("%lld rounds on a %lld by %lld grid: scores sum to %lld, checksum %lld\n", (long long)rounds,
           (long long)size, (long long)size, (long long)total, (long long)check);
    for (int64_t i = 0; i < size; i++) {
        free(grid[i]);
    }
    free(grid);
    return 0;
}
