/* Benchmark mirror of lisscan.kara — LeetCode #300, Longest Increasing
 * Subsequence. Same patience sorting, same hand-written binary search, same
 * reused stack tails buffer. See ../README.md § Benchmarks. */
#include <stdio.h>
#include <stdlib.h>

#define N_ARRAYS 3000
#define LEN      512
#define PASSES   24
#define SPREAD   4096

static long lcg(long state) {
    return (state * 1103515245 + 12345) & 0x7fffffff;
}

int main(void) {
    long total = (long)N_ARRAYS * LEN;
    long *data = malloc(sizeof(long) * total);
    if (!data) return 1;

    long state = 20300;
    for (long i = 0; i < total; i++) {
        state = lcg(state);
        data[i] = (state / 65536) % SPREAD;
    }

    long tails[LEN];
    long checksum = 0;

    for (int pass = 0; pass < PASSES; pass++) {
        for (long a = 0; a < N_ARRAYS; a++) {
            long base = a * LEN;
            long n_tails = 0;

            for (long k = 0; k < LEN; k++) {
                long x = data[base + k];

                /* size_t, not long: the idiomatic C index type, and the fair one.
               With signed `long` here clang emits the sign-correction sequence
               for `/ 2` and the lane costs 1.249 s instead of 950 ms — a 1.31x
               handicap this mirror should not be carrying. See ../README.md. */
            size_t lo = 0, hi = (size_t)n_tails;
                while (lo < hi) {
                    size_t mid = lo + (hi - lo) / 2;
                    if (tails[mid] < x) lo = mid + 1;
                    else hi = mid;
                }

                if (lo == (size_t)n_tails) tails[n_tails++] = x;
                else tails[lo] = x;
            }

            checksum = (checksum * 31 + n_tails) % 1000000007;
        }
    }

    printf("arrays %d len %d passes %d checksum %ld\n", N_ARRAYS, LEN, PASSES, checksum);
    free(data);
    return 0;
}
