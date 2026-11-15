// LeetCode #1582 bench: the same row and column sums, in C. Each row is its
// own allocation, and the two sum buffers are malloc'd per call, as in the
// Kara arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t num_special(int64_t **mat, int64_t m, int64_t n) {
    int64_t *rows = malloc(m * sizeof(int64_t));
    int64_t *cols = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) {
        int64_t s = 0;
        for (int64_t j = 0; j < n; j++) s += mat[i][j];
        rows[i] = s;
    }
    for (int64_t j = 0; j < n; j++) {
        int64_t s = 0;
        for (int64_t i = 0; i < m; i++) s += mat[i][j];
        cols[j] = s;
    }
    int64_t count = 0;
    for (int64_t i = 0; i < m; i++)
        for (int64_t j = 0; j < n; j++)
            if (mat[i][j] == 1 && rows[i] == 1 && cols[j] == 1) count++;
    free(rows);
    free(cols);
    return count;
}

static int64_t seed = 1582;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    enum { P = 2000, N = 100 };
    int64_t **mats[P];
    for (int p = 0; p < P; p++) {
        mats[p] = malloc(N * sizeof(int64_t *));
        for (int i = 0; i < N; i++) {
            mats[p][i] = malloc(N * sizeof(int64_t));
            for (int j = 0; j < N; j++) mats[p][i][j] = next_random() % 100 == 0 ? 1 : 0;
        }
    }
    int64_t check = 0, total = 0;
    for (int p = 0; p < P; p++) {
        int64_t special = num_special(mats[p], N, N);
        total += special;
        check = mix(check, special);
    }
    printf("2000 matrices of 100 x 100: special positions %lld, checksum %lld\n", (long long)total, (long long)check);
    for (int p = 0; p < P; p++) {
        for (int i = 0; i < N; i++) free(mats[p][i]);
        free(mats[p]);
    }
    return 0;
}
