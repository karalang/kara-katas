// LeetCode #2373: Largest Local Values in a Matrix -- the bench, the ★ arm
// in C: each cell of the answer is the largest of the nine values in the
// 3 x 3 block whose top left corner it names. The answer's rows are
// allocated one by one, as the other languages' are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t **largest_local(int64_t **grid, int64_t n) {
    int64_t **out = malloc((n - 2) * sizeof(int64_t *));
    for (int64_t i = 0; i < n - 2; i++) {
        out[i] = malloc((n - 2) * sizeof(int64_t));
        for (int64_t j = 0; j < n - 2; j++) {
            int64_t most = 0;
            for (int di = 0; di < 3; di++) {
                for (int dj = 0; dj < 3; dj++) {
                    if (grid[i + di][j + dj] > most) {
                        most = grid[i + di][j + dj];
                    }
                }
            }
            out[i][j] = most;
        }
    }
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // grid a: 100 x 100 random values from 1 to 10 (a + 1)
    const int64_t n = 100;
    int64_t seed = 2373;
    int64_t **grids[10];
    for (int64_t a = 0; a < 10; a++) {
        grids[a] = malloc(n * sizeof(int64_t *));
        for (int64_t i = 0; i < n; i++) {
            grids[a][i] = malloc(n * sizeof(int64_t));
            for (int64_t j = 0; j < n; j++) {
                grids[a][i][j] = 1 + next_random(&seed) % (10 * (a + 1));
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 200; p++) {
        for (int a = 0; a < 10; a++) {
            int64_t **out = largest_local(grids[a], n);
            for (int64_t i = 0; i < n - 2; i++) {
                for (int64_t j = 0; j < n - 2; j++) {
                    check = (check * 31 + out[i][j] + p) % 1000000007;
                }
                free(out[i]);
            }
            free(out);
        }
    }
    printf("200 passes over 10 grids of 100 x 100: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) {
        for (int64_t i = 0; i < n; i++) {
            free(grids[a][i]);
        }
        free(grids[a]);
    }
    return 0;
}
