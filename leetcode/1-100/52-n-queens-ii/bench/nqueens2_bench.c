/* Bench mirror of nqueens2_bench.kara — return-value counting backtracker,
 * weighted-checksum i64 sink, swept over n = 9..13. clang -O3.
 * See ../README.md § Benchmarks. */
#include <stdio.h>
#include <stdint.h>

static int64_t search(int64_t n, int64_t row, int64_t cols, int64_t diag1, int64_t diag2,
                      int64_t partial) {
    if (row == n) {
        return 1 + partial;
    }
    int64_t acc = 0;
    for (int64_t c = 0; c < n; c++) {
        int64_t bit_c = 1LL << c;
        int64_t bit_d1 = 1LL << (row + c);
        int64_t bit_d2 = 1LL << (row - c + (n - 1));
        if ((cols & bit_c) == 0 && (diag1 & bit_d1) == 0 && (diag2 & bit_d2) == 0) {
            acc += search(n, row + 1, cols | bit_c, diag1 | bit_d1, diag2 | bit_d2,
                          partial + c * (row + 1));
        }
    }
    return acc;
}

int main(void) {
    int64_t n_lo = 9, n_hi = 13;
    int64_t total = 0;
    for (int64_t n = n_lo; n <= n_hi; n++) {
        total += search(n, 0, 0, 0, 0, 0);
    }
    printf("%lld\n", (long long)total);
    return 0;
}
