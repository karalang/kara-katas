#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// the tables as arrays of rows, each row malloc'd, as the Kāra and Rust
// programs hold a Vec of Vecs
static int64_t **table(int64_t rows, int64_t cols) {
    int64_t **t = malloc(rows * sizeof(int64_t *));
    for (int64_t r = 0; r < rows; r++) t[r] = calloc(cols, sizeof(int64_t));
    return t;
}

static void release(int64_t **t, int64_t rows) {
    for (int64_t r = 0; r < rows; r++) free(t[r]);
    free(t);
}

static int32_t num_of_arrays(int32_t n, int32_t m, int32_t k) {
    const int64_t modulus = 1000000007;
    int64_t **ways = table(m + 1, k + 1);
    if (k >= 1)
        for (int64_t j = 1; j <= m; j++) ways[j][1] = 1;
    for (int32_t i = 1; i < n; i++) {
        int64_t **next = table(m + 1, k + 1);
        for (int64_t c = 1; c <= k; c++) {
            int64_t below = 0;
            for (int64_t j = 1; j <= m; j++) {
                next[j][c] = (ways[j][c] * j + below) % modulus;
                below = (below + ways[j][c - 1]) % modulus;
            }
        }
        release(ways, m + 1);
        ways = next;
    }
    int64_t total = 0;
    for (int64_t j = 1; j <= m; j++) total = (total + ways[j][k]) % modulus;
    release(ways, m + 1);
    return (int32_t)total;
}

int main(void) {
    int64_t seed = 1420, check = 0;
    for (int i = 0; i < 1000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t k = seed / 65536 % 51;
        check = (check * 131 + num_of_arrays(50, 100, (int32_t)k)) % 1000000007;
    }
    printf("1000 values of k at n = 50, m = 100: checksum %lld\n", (long long)check);
    return 0;
}
