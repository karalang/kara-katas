/* Bench mirror of maxsub_bench.kara — Kadane over a batch of LCG-generated arrays,
 * i64 sink of per-array answers. clang -O3. See ../README.md § Benchmarks. */
#include <stdio.h>
#include <stdint.h>

int main(void) {
    int64_t m = 1103515245;       /* glibc LCG multiplier */
    int64_t inc = 12345;          /* glibc LCG increment */
    int64_t modulus = 2147483648; /* 2^31 */
    int64_t windows = 120000;     /* number of simulated input arrays */
    int64_t w = 1000;             /* length of each array */

    int64_t state = 1;            /* LCG seed */
    int64_t sink = 0;
    for (int64_t k = 0; k < windows; k++) {
        state = (state * m + inc) % modulus;
        int64_t v0 = (state % 100) - 50;
        int64_t best = v0;
        int64_t here = v0;
        for (int64_t j = 1; j < w; j++) {
            state = (state * m + inc) % modulus;
            int64_t v = (state % 100) - 50;
            here = (here + v > v) ? (here + v) : v;
            if (here > best) {
                best = here;
            }
        }
        sink += best;
    }
    printf("%lld\n", (long long)sink);
    return 0;
}
