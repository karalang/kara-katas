// LeetCode #1139: Largest 1-Bordered Square -- the bench, the ★ arm's
// algorithm: runs of 1s left and up, each corner's sides tried from the longest down.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100

static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t largest1_bordered_square(int64_t **grid, int64_t rows, int64_t cols) {
    int64_t **left = malloc(rows * sizeof(int64_t *));
    int64_t **up = malloc(rows * sizeof(int64_t *));
    for (int64_t i = 0; i < rows; i++) {
        left[i] = calloc(cols, sizeof(int64_t));
        up[i] = calloc(cols, sizeof(int64_t));
    }
    for (int64_t i = 0; i < rows; i++)
        for (int64_t j = 0; j < cols; j++)
            if (grid[i][j] == 1) {
                left[i][j] = j > 0 ? left[i][j - 1] + 1 : 1;
                up[i][j] = i > 0 ? up[i - 1][j] + 1 : 1;
            }
    int64_t best = 0;
    for (int64_t i = 0; i < rows; i++)
        for (int64_t j = 0; j < cols; j++) {
            int64_t k = min64(left[i][j], up[i][j]);
            while (k > best) {
                if (left[i - k + 1][j] >= k && up[i][j - k + 1] >= k) best = k;
                k--;
            }
        }
    for (int64_t i = 0; i < rows; i++) {
        free(left[i]);
        free(up[i]);
    }
    free(left);
    free(up);
    return best * best;
}

static int64_t seed = 1139;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t **grids[20];
    for (int g = 0; g < 20; g++) {
        grids[g] = malloc(N * sizeof(int64_t *));
        for (int i = 0; i < N; i++) {
            grids[g][i] = malloc(N * sizeof(int64_t));
            for (int j = 0; j < N; j++) grids[g][i][j] = next_random() % 100 < 95 ? 1 : 0;
        }
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < 300; r++)
        for (int g = 0; g < 20; g++) {
            int64_t i = next_random() % 100;
            int64_t j = next_random() % 100;
            grids[g][i][j] = 1 - grids[g][i][j];
            int64_t area = largest1_bordered_square(grids[g], N, N);
            total += area;
            check = (check * 131 + area + 1) % 1000000007;
        }
    printf("300 rounds over 20 grids of 100 by 100: areas total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
