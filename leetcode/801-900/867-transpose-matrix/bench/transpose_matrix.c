// LeetCode #867: Transpose Matrix -- C mirror of the bench program (the ★
// arm, one column at a time). Rows are separate allocations, as in
// LeetCode's `int**` signature, with 64-bit entries as in the Kāra program.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t **transpose(int64_t **matrix, int64_t rows, int64_t cols) {
    int64_t **out = malloc(cols * sizeof(int64_t *));
    for (int64_t c = 0; c < cols; c++) {
        int64_t *row = malloc(rows * sizeof(int64_t));
        for (int64_t r = 0; r < rows; r++) row[r] = matrix[r][c];
        out[c] = row;
    }
    return out;
}

static void release(int64_t **m, int64_t rows) {
    for (int64_t r = 0; r < rows; r++) free(m[r]);
    free(m);
}

static int64_t seed = 867;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t random_value(void) {
    int64_t hi = next_random();
    int64_t lo = next_random();
    return (hi * 32768 + lo) % 2000000001 - 1000000000;
}

int main(void) {
    int64_t rows = 1000, cols = 100;
    int64_t **m = malloc(rows * sizeof(int64_t *));
    for (int64_t r = 0; r < rows; r++) {
        m[r] = malloc(cols * sizeof(int64_t));
        for (int64_t c = 0; c < cols; c++) m[r][c] = random_value();
    }
    int64_t rounds = 6000;
    int64_t check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t **t = transpose(m, rows, cols);
        release(m, rows);
        m = t;
        int64_t tmp = rows;
        rows = cols;
        cols = tmp;
        int64_t r = round * 7 % rows;
        int64_t c = round * 13 % cols;
        check = (check * 31 + m[r][c] % 1000000007 + 1000000007) % 1000000007;
    }
    for (int64_t r = 0; r < rows; r++)
        for (int64_t c = 0; c < cols; c++)
            check = (check * 31 + m[r][c] % 1000000007 + 1000000007) % 1000000007;
    printf("%lld transposes of a 1000 x 100 matrix: %lld x %lld, checksum %lld\n",
           (long long)rounds, (long long)rows, (long long)cols, (long long)check);
    release(m, rows);
    return 0;
}
