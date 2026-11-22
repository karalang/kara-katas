// LeetCode #2718: Sum of Matrix After Queries -- the bench (matrix.kara
// in C): the queries read from the last back, each row or column not set
// later filling the lines of the other kind not yet taken.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t matrix_sum_queries(int64_t n, const int64_t (*queries)[3], int64_t q) {
    bool *row_taken = calloc((size_t)n, sizeof(bool));
    bool *col_taken = calloc((size_t)n, sizeof(bool));
    int64_t rows_left = n, cols_left = n, sum = 0;
    for (int64_t k = q - 1; k >= 0; k--) {
        int64_t kind = queries[k][0], index = queries[k][1], value = queries[k][2];
        if (kind == 0) {
            if (!row_taken[index]) {
                row_taken[index] = true;
                rows_left--;
                sum += value * cols_left;
            }
        } else if (!col_taken[index]) {
            col_taken[index] = true;
            cols_left--;
            sum += value * rows_left;
        }
    }
    free(row_taken);
    free(col_taken);
    return sum;
}

static int64_t seed = 2718;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int count = 40, rounds = 20, q = 50000;
    const int64_t n = 10000;
    int64_t (*queries)[3] = malloc(sizeof(int64_t[3]) * (size_t)count * q);
    for (int c = 0; c < count; c++) {
        for (int k = 0; k < q; k++) {
            int64_t *row = queries[(size_t)c * q + k];
            row[0] = next_random() % 2;
            row[1] = wide() % n;
            row[2] = wide() % 100001;
        }
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int c = 0; c < count; c++) {
            int64_t total = matrix_sum_queries(n, queries + (size_t)c * q, q);
            sum += total % 1000000007;
            check = (check * 31 + total % 1000000007 + r) % 1000000007;
        }
    }
    printf("%d cases of 50000 queries on 10000 rows, %d rounds: sums mod p sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(queries);
    return 0;
}
