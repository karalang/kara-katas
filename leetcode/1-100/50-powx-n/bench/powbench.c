/* Bench mirror of powbench.kara — recursive fast-power, f64-bits sum sink.
 * clang -O3. See ../README.md § Benchmarks. */
#include <stdio.h>
#include <stdint.h>
#include <string.h>

static double fast_pow(double x, int64_t n) {
    if (n == 0) return 1.0;
    double half = fast_pow(x, n / 2);
    return (n % 2 == 0) ? half * half : half * half * x;
}

static double my_pow(double x, int64_t n) {
    return (n < 0) ? 1.0 / fast_pow(x, -n) : fast_pow(x, n);
}

static uint64_t to_bits(double x) {
    uint64_t b;
    memcpy(&b, &x, sizeof b);
    return b;
}

int main(void) {
    int64_t n_iters = 400000, k_reps = 20;
    double inv2048 = 0.00048828125; /* 2^-11, exact */
    uint64_t acc = 0;
    for (int64_t rep = 0; rep < k_reps; rep++) {
        for (int64_t i = 0; i < n_iters; i++) {
            int64_t h = ((i + rep * 7919) * 2654435761) & 2047;
            double x = 1.0 + (double)h * inv2048;
            int64_t n = ((i + rep) % 129) - 64;
            acc += to_bits(my_pow(x, n));
        }
    }
    printf("%llu\n", (unsigned long long)(acc & 0x7FFFFFFFFFFFFFFFULL));
    return 0;
}
