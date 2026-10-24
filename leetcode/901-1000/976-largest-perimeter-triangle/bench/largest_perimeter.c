// Benchmark: LeetCode #976 Largest Perimeter Triangle -- the ★ arm, sort
// and scan from the top, on 20 lists of 10000 random lengths. Mirrors
// largest_perimeter.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 10000
#define COUNT 20

static int by_value(const void *a, const void *b) {
    int64_t p = *(const int64_t *)a, q = *(const int64_t *)b;
    return (p > q) - (p < q);
}

static int64_t largest_perimeter(const int64_t *nums, int64_t n, int64_t *a) {
    memcpy(a, nums, (size_t)n * sizeof(int64_t));
    qsort(a, (size_t)n, sizeof(int64_t), by_value);
    for (int64_t i = n - 1; i >= 2; i--) {
        if (a[i - 2] + a[i - 1] > a[i]) return a[i - 2] + a[i - 1] + a[i];
    }
    return 0;
}

static int64_t seed = 976;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t lists[COUNT][N];

int main(void) {
    int64_t rounds = 50;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) {
            int64_t hi = next_random();
            lists[c][i] = 1 + (hi * 32768 + next_random()) % 1000000;
        }
    }
    static int64_t scratch[N];
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < COUNT; i++) {
            int64_t p = largest_perimeter(lists[(r + i) % COUNT], N, scratch);
            total += p;
            check = (check * 31 + p) % 1000000007;
        }
    }
    printf("%lld rounds over %d lists of 10000 lengths: perimeters total %lld, checksum %lld\n",
           (long long)rounds, COUNT, (long long)total, (long long)check);
    return 0;
}
