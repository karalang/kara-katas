// LeetCode #1292 bench: the ★ arm over 20 matrices of 300 by 300 with values
// up to 100, built once; then 100 passes, each setting one cell of every
// matrix and its threshold from the checksum so far and answering it. The
// prefix table is a fresh zeroed allocation per call, rows of n + 1, as the
// other languages' tables are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { M = 300, N = 300, MATS = 20 };

static int64_t max_side_length(int64_t **mat, int m, int n, int64_t threshold) {
    int64_t **sum = malloc(sizeof(int64_t *) * (m + 1));
    for (int i = 0; i <= m; i++) {
        sum[i] = calloc(n + 1, sizeof(int64_t));
    }
    int best = 0;
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            sum[i][j] = mat[i - 1][j - 1] + sum[i - 1][j] + sum[i][j - 1] - sum[i - 1][j - 1];
            int k = best + 1;
            if (i >= k && j >= k && sum[i][j] - sum[i - k][j] - sum[i][j - k] + sum[i - k][j - k] <= threshold) {
                best = k;
            }
        }
    }
    for (int i = 0; i <= m; i++) {
        free(sum[i]);
    }
    free(sum);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1292;
    int64_t **mats[MATS];
    for (int a = 0; a < MATS; a++) {
        mats[a] = malloc(sizeof(int64_t *) * M);
        for (int i = 0; i < M; i++) {
            mats[a][i] = malloc(sizeof(int64_t) * N);
            for (int j = 0; j < N; j++) {
                mats[a][i][j] = next_random(&seed) % 101;
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 100; p++) {
        for (int a = 0; a < MATS; a++) {
            mats[a][check % 300][(check / 300) % 300] = check % 101;
            int64_t threshold = check % 100001;
            check = (check * 31 + max_side_length(mats[a], M, N, threshold) + p) % 1000000007;
        }
    }
    printf("100 passes over 20 matrices of 300 by 300: checksum %lld\n", (long long)check);
    return 0;
}
