// Benchmark for #598: C mirror of the ★ arm (the smallest corner); see
// max_count.kara. The operations are LeetCode's C shape, an `int64_t **`
// with each operation its own `malloc`'d pair.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_count(int64_t m, int64_t n, int64_t **ops, int k) {
    int64_t rows = m, cols = n;
    for (int i = 0; i < k; i++) {
        if (ops[i][0] < rows)
            rows = ops[i][0];
        if (ops[i][1] < cols)
            cols = ops[i][1];
    }
    return rows * cols;
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t hi = step(seed);
    int64_t lo = step(seed);
    return hi * 32768 + lo;
}

int main(void) {
    enum { COUNT = 100, ROUNDS = 300, K = 10000 };
    int64_t seed = 598;
    static int64_t sizes[COUNT][2];
    static int64_t **lists[COUNT];
    for (int c = 0; c < COUNT; c++) {
        int64_t m = 1 + wide(&seed) % 40000;
        int64_t n = 1 + wide(&seed) % 40000;
        lists[c] = malloc(K * sizeof(int64_t *));
        for (int j = 0; j < K; j++) {
            lists[c][j] = malloc(2 * sizeof(int64_t));
            lists[c][j][0] = m - step(&seed) % (1 + m / 8);
            lists[c][j][1] = n - step(&seed) % (1 + n / 8);
        }
        sizes[c][0] = m;
        sizes[c][1] = n;
    }
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < ROUNDS; round++)
        for (int g = 0; g < COUNT; g++) {
            int c = (round * 7 + g) % COUNT;
            int64_t got = max_count(sizes[c][0], sizes[c][1], lists[c], K);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    printf("%d lists, %d rounds: total %lld, checksum %lld\n", COUNT, ROUNDS, (long long)total,
           (long long)checksum);
    return 0;
}
