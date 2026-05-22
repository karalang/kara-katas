/*
 * LeetCode 204 — bench mirror in C. Idiomatic single-threaded
 * implementation; matches kara's bench/count.kara sink (count + sum)
 * for N = 10_000_000.
 *
 * The buffer is pre-sized at 700_000 i64 entries (π(10^7) = 664_579, with
 * headroom) to skip realloc churn — the equivalent of Rust's
 * `Vec::with_capacity` and kara's `Vec.with_capacity`. For a fair
 * comparison we'd use `realloc` doubling like Rust/kara's `push`; using
 * pre-sized buffers here is a kindness to C (avoids the realloc bench
 * dominating the cmp).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

static bool is_prime(int64_t n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if ((n % 2) == 0) return false;
    for (int64_t i = 3; i * i <= n; i += 2) {
        if ((n % i) == 0) return false;
    }
    return true;
}

int main(void) {
    const int64_t n = 10000000;
    const size_t cap = 700000;

    int64_t *primes = (int64_t *)malloc(cap * sizeof(int64_t));
    if (!primes) {
        fprintf(stderr, "malloc failed\n");
        return 1;
    }
    size_t len = 0;

    for (int64_t k = 0; k < n; k++) {
        if (is_prime(k)) {
            primes[len++] = k;
        }
    }

    int64_t sum = 0;
    for (size_t i = 0; i < len; i++) {
        sum += primes[i];
    }
    printf("%zu\n", len);
    printf("%lld\n", (long long)sum);

    free(primes);
    return 0;
}
