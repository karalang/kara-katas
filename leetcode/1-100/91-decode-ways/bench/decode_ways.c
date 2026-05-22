// LeetCode #91 — C bench peer for decode_ways.kara. Single-file clang -O3
// build. Same algorithm, same workload, same sink as the Kara/Rust mirrors.

#include <stdint.h>
#include <stdio.h>

#define L 80
#define N_ITERS 10000000
#define MODULUS 1000000007LL

static int64_t decode_ways(const unsigned char *bytes, int64_t n) {
    if (n == 0) return 0;
    const unsigned char zero = '0';
    if (bytes[0] == zero) return 0;

    int64_t prev2 = 1;
    int64_t prev1 = 1;

    for (int64_t i = 1; i < n; i++) {
        int32_t d1 = (int32_t)bytes[i] - (int32_t)zero;
        int32_t d0 = (int32_t)bytes[i - 1] - (int32_t)zero;
        int32_t two = d0 * 10 + d1;

        int64_t cur = 0;
        if (d1 >= 1 && d1 <= 9) {
            cur += prev1;
        }
        if (two >= 10 && two <= 26) {
            cur += prev2;
        }

        prev2 = prev1;
        prev1 = cur;
    }

    return prev1;
}

int main(void) {
    static unsigned char buf[L];
    const unsigned char zero = '0';
    for (int64_t j = 0; j < L; j++) {
        int64_t d = ((j * 3) % 9) + 1;
        buf[j] = zero + (unsigned char)d;
    }

    int64_t sum = 0;
    for (int64_t k = 0; k < N_ITERS; k++) {
        int64_t pos = k % L;
        int64_t d = ((k * 11) % 9) + 1;
        buf[pos] = zero + (unsigned char)d;
        sum = (sum + decode_ways(buf, L)) % MODULUS;
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
