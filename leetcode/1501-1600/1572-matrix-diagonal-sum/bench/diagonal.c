// LeetCode #1572: Matrix Diagonal Sum -- bench: the ★ arm (two cells a
// row, the centre taken off once) over one matrix of 1001 rows of values
// from 1 to 100, built once; then 200000 rounds, each writing one random
// cell and summing the diagonals again.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t diagonal_sum(int64_t **mat, int64_t n) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        total += mat[i][i] + mat[i][n - 1 - i];
    }
    if (n % 2 == 1) {
        total -= mat[n / 2][n / 2];
    }
    return total;
}

static int64_t seed = 1572;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    const int64_t n = 1001;
    const int64_t rounds = 200000;
    int64_t **mat = malloc(sizeof(int64_t *) * n);
    for (int64_t i = 0; i < n; i++) {
        mat[i] = malloc(sizeof(int64_t) * n);
        for (int64_t j = 0; j < n; j++) {
            mat[i][j] = next_random() % 100 + 1;
        }
    }
    int64_t check = 0, total = 0;
    for (int64_t k = 0; k < rounds; k++) {
        int64_t r = next_random() % n;
        int64_t c = next_random() % n;
        mat[r][c] = next_random() % 100 + 1;
        int64_t sum = diagonal_sum(mat, n);
        total += sum;
        check = mix(check, sum);
    }
    printf("%lld rounds on %lld rows: sums total %lld, checksum %lld\n", (long long)rounds, (long long)n,
           (long long)total, (long long)check);
    for (int64_t i = 0; i < n; i++) {
        free(mat[i]);
    }
    free(mat);
    return 0;
}
