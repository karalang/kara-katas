// Benchmark workload for LeetCode #266 — Palindrome Permutation (C mirror).
// Mirrors pal_perm.kara algorithm-for-algorithm.
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n = 200000, rounds = 4000, span = 1000;
    long width = n - span;

    long *data = malloc(n * sizeof(long));
    long state = 266266;
    for (long z = 0; z < n; z++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        data[z] = 97 + (state / 65536L) % 26;
    }

    // Heap, not a stack array — matching the Vec/slice the other three mirrors
    // use. On the stack this is the only mirror whose counter table moves with
    // the frame layout, and `-march=x86-64-v3` shifts it by 64 bytes, which was
    // worth 23% on an otherwise instruction-identical loop. See ../README.md.
    long *counts = malloc(256 * sizeof(long));

    long sink = 0;
    for (long r = 0; r < rounds; r++) {
        for (long c = 0; c < 256; c++) counts[c] = 0;

        long start = (r * 7919L) % span;
        long stop = start + width;
        for (long i = start; i < stop; i++) {
            long b = data[i];
            counts[b] += 1;
        }

        long odd = 0;
        for (long k = 0; k < 256; k++) if (counts[k] % 2 == 1) odd++;
        long verdict = (odd <= 1) ? 1 : 0;
        sink = (sink * 131 + odd * 7 + verdict) % 1000000007L;
    }

    printf("%ld\n", sink);
    free(data); free(counts);
    return 0;
}
