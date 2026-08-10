// Benchmark workload for LeetCode #254 — Factor Combinations (C mirror).
// Mirrors factor_combinations.kara algorithm-for-algorithm.
//
// Each combination is MATERIALISED into its own heap array before hashing, the
// same as the Kara and Rust mirrors. Hashing inline off the path would skip the
// per-combination allocation that is a deliberate part of this workload and make
// the C row artificially fast.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long digest = 0, total = 0;
static long path[64]; static int plen = 0;

static void helper(long remaining, long start) {
    long i = start;
    while (i * i <= remaining) {
        if (remaining % i == 0) {
            int n = plen + 2;
            long *combo = malloc(n * sizeof(long));
            memcpy(combo, path, plen * sizeof(long));
            combo[plen] = i;
            combo[plen + 1] = remaining / i;

            long h = 1;
            for (int k = 0; k < n; k++) h = (h * 1000003L + combo[k]) % 1000000007L;
            digest = (digest + h) % 1000000007L;
            total++;
            free(combo);

            path[plen++] = i;
            helper(remaining / i, i);
            plen--;
        }
        i++;
    }
}

int main(void) {
    long hi = 150000;
    for (long n = 2; n <= hi; n++) {
        plen = 0;
        if (n >= 4) helper(n, 2);
    }
    printf("%ld %ld\n", total, digest);
    return 0;
}
