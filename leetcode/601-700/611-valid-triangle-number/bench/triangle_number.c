// Benchmark for #611: the ★ arm (sort, then two pointers); see
// triangle_number.kara. Each call sorts a `malloc`'d copy with `qsort`,
// as the Kāra arm sorts a clone, and frees it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    return (a > b) - (a < b);
}

static int64_t triangle_number(const int64_t *nums, int64_t n) {
    int64_t *a = malloc((size_t)n * sizeof(int64_t));
    memcpy(a, nums, (size_t)n * sizeof(int64_t));
    qsort(a, (size_t)n, sizeof(int64_t), cmp);
    int64_t count = 0;
    for (int64_t k = 2; k < n; k++) {
        int64_t i = 0, j = k - 1;
        while (i < j) {
            if (a[i] + a[j] > a[k]) {
                count += j - i;
                j--;
            } else {
                i++;
            }
        }
    }
    free(a);
    return count;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { ARRAYS = 20, ROUNDS = 600, N = 1000 };
    int64_t seed = 611;
    static int64_t all[ARRAYS][N];
    for (int c = 0; c < ARRAYS; c++) {
        int64_t bound = 100 + step(&seed) % 901;
        for (int k = 0; k < N; k++) all[c][k] = step(&seed) % (bound + 1);
    }
    int64_t total = 0, checksum = 0;
    for (int r = 0; r < ROUNDS; r++) {
        int64_t got = triangle_number(all[(r * 7) % ARRAYS], N);
        total += got;
        checksum = (checksum * 31 + got) % 1000000007;
    }
    printf("%d arrays, %d rounds: %lld triangles, checksum %lld\n", ARRAYS, ROUNDS, (long long)total,
           (long long)checksum);
    return 0;
}
