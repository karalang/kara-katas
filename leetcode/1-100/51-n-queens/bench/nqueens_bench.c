/* Bench mirror of nqueens_bench.kara — bitmask solution-counting backtracker,
 * weighted-checksum i64 sink, swept over n = 8..13. clang -O3.
 * See ../README.md § Benchmarks. */
#include <stdio.h>
#include <stdint.h>

static void count(int64_t n, int64_t row, int64_t cols, int64_t diag1, int64_t diag2,
                  int64_t partial, int64_t *acc, int64_t *sink) {
    if (row == n) {
        *acc += 1;
        *sink += partial;
        return;
    }
    for (int64_t c = 0; c < n; c++) {
        int64_t bit_c = 1LL << c;
        int64_t bit_d1 = 1LL << (row + c);
        int64_t bit_d2 = 1LL << (row - c + (n - 1));
        if ((cols & bit_c) == 0 && (diag1 & bit_d1) == 0 && (diag2 & bit_d2) == 0) {
            count(n, row + 1, cols | bit_c, diag1 | bit_d1, diag2 | bit_d2,
                  partial + c * (row + 1), acc, sink);
        }
    }
}

int main(void) {
    int64_t n_lo = 8, n_hi = 13;
    int64_t total = 0;
    for (int64_t n = n_lo; n <= n_hi; n++) {
        int64_t acc = 0, sink = 0;
        count(n, 0, 0, 0, 0, 0, &acc, &sink);
        total += acc * 100003 + sink;
    }
    printf("%lld\n", (long long)total);
    return 0;
}
