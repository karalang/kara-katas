#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int by_value(const void *x, const void *y) {
    int32_t a = *(const int32_t *)x, b = *(const int32_t *)y;
    return (a > b) - (a < b);
}

/* The sums of each round in a fresh array, sorted with the C library's
   qsort, as the Kara arm sorts a fresh Vec. */
static int32_t kth_smallest(int32_t mat[40][40], int m, int n, int32_t k) {
    int32_t *sums = malloc(sizeof(int32_t));
    int64_t count = 1;
    sums[0] = 0;
    for (int r = 0; r < m; r++) {
        int32_t *next = malloc(sizeof(int32_t) * (size_t)(count * n));
        int64_t len = 0;
        for (int64_t i = 0; i < count; i++)
            for (int j = 0; j < n; j++) next[len++] = sums[i] + mat[r][j];
        qsort(next, (size_t)len, sizeof(int32_t), by_value);
        free(sums);
        sums = next;
        count = len < k ? len : k;
    }
    int32_t answer = sums[k - 1];
    free(sums);
    return answer;
}

int main(void) {
    int64_t seed = 1439, check = 0;
    static int32_t mat[40][40];
    for (int c = 0; c < 300; c++) {
        for (int r = 0; r < 40; r++) {
            for (int j = 0; j < 40; j++) {
                seed = (seed * 1103515245 + 12345) % 2147483648;
                mat[r][j] = (int32_t)(1 + seed / 65536 % 5000);
            }
            qsort(mat[r], 40, sizeof(int32_t), by_value);
        }
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int32_t k = (int32_t)(1 + seed / 65536 % 200);
        check = (check * 131 + kth_smallest(mat, 40, 40, k)) % 1000000007;
    }
    printf("300 matrices of 40 by 40: checksum %lld\n", (long long)check);
    return 0;
}
