// Benchmark: LeetCode #977 Squares of a Sorted Array -- the ★ arm, two
// pointers from the ends, on 20 sorted arrays of 10000 numbers. Mirrors
// sorted_squares.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 10000
#define COUNT 20

static int by_value(const void *a, const void *b) {
    int64_t p = *(const int64_t *)a, q = *(const int64_t *)b;
    return (p > q) - (p < q);
}

static void sorted_squares(const int64_t *nums, int64_t n, int64_t *out) {
    int64_t lo = 0, hi = n - 1, at = n - 1;
    while (lo <= hi) {
        int64_t a = nums[lo] * nums[lo];
        int64_t b = nums[hi] * nums[hi];
        if (a > b) {
            out[at] = a;
            lo++;
        } else {
            out[at] = b;
            hi--;
        }
        at--;
    }
}

static int64_t seed = 977;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t arrays[COUNT][N];

int main(void) {
    int64_t rounds = 500;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) arrays[c][i] = next_random() % 20001 - 10000;
        qsort(arrays[c], N, sizeof(int64_t), by_value);
    }
    static int64_t out[N];
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < COUNT; i++) {
            sorted_squares(arrays[(r + i) % COUNT], N, out);
            total += out[0] + out[N - 1];
            check = (check * 31 + out[(r * 13 + i * 7) % N]) % 1000000007;
        }
    }
    printf("%lld rounds over %d arrays of 10000 numbers: squares total %lld, checksum %lld\n",
           (long long)rounds, COUNT, (long long)total, (long long)check);
    return 0;
}
