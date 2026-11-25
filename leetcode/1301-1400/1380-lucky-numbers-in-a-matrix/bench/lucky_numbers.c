// LeetCode #1380 bench -- C: the ★ arm: each row's least value and each
// column's greatest found in one pass, then every cell that is both.

#include <limits.h>
#include <stdint.h>
#include <stdio.h>

#define N 50

// writes the lucky numbers to `lucky` and returns how many
static int lucky_numbers(int m, int n, int matrix[N][N], int *lucky) {
    int row_min[N], col_max[N];
    for (int i = 0; i < m; i++) {
        row_min[i] = INT_MAX;
    }
    for (int j = 0; j < n; j++) {
        col_max[j] = INT_MIN;
    }
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (matrix[i][j] < row_min[i]) {
                row_min[i] = matrix[i][j];
            }
            if (matrix[i][j] > col_max[j]) {
                col_max[j] = matrix[i][j];
            }
        }
    }
    int count = 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (matrix[i][j] == row_min[i] && matrix[i][j] == col_max[j]) {
                lucky[count++] = matrix[i][j];
            }
        }
    }
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int grids[20][N][N];

int main(void) {
    // 20 matrices of 50 by 50 built once; then 20000 rounds, each swapping
    // two cells of one matrix and finding its lucky numbers (see the Kāra
    // bench)
    const int64_t n = N;
    int64_t seed = 1380;
    int lucky[N * N];
    for (int g = 0; g < 20; g++) {
        for (int64_t i = 0; i < n; i++) {
            for (int64_t j = 0; j < n; j++) {
                grids[g][i][j] = (int)(i * n + j + 1);
            }
        }
        for (int s = 0; s < 300; s++) {
            int64_t a = next_random(&seed) % (n * n);
            int64_t b = next_random(&seed) % (n * n);
            int t = grids[g][a / n][a % n];
            grids[g][a / n][a % n] = grids[g][b / n][b % n];
            grids[g][b / n][b % n] = t;
        }
    }
    int64_t check = 0;
    for (int64_t r = 0; r < 20000; r++) {
        int64_t g = check % 20;
        int64_t a = (check / 20) % (n * n);
        int64_t b = (check / 7 + r) % (n * n);
        int t = grids[g][a / n][a % n];
        grids[g][a / n][a % n] = grids[g][b / n][b % n];
        grids[g][b / n][b % n] = t;
        int count = lucky_numbers(N, N, grids[g], lucky);
        int64_t got = count;
        for (int k = 0; k < count; k++) {
            got = got * 2503 + lucky[k];
        }
        check = (check * 31 + got + r) % 1000000007;
    }
    printf("20000 rounds over 20 matrices of 50 by 50: checksum %lld\n", (long long)check);
    return 0;
}
