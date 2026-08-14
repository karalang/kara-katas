// Benchmark workload for LeetCode #267 — Palindrome Permutation II (C mirror).
// Mirrors pal_gen.kara algorithm-for-algorithm, including the hoisted output
// buffer (see that file for why no mirror builds a string per leaf).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void build(long *counts, long *half, long depth, long half_len,
                  long middle, long *buf, long *acc) {
    if (depth == half_len) {
        long n = 0;
        for (long i = 0; i < half_len; i++) buf[n++] = half[i];
        if (middle >= 0) buf[n++] = middle;
        for (long j = half_len - 1; j >= 0; j--) buf[n++] = half[j];
        for (long k = 0; k < n; k++)
            *acc = (*acc * 31 + buf[k]) % 1000000007L;
        return;
    }
    for (long c = 0; c < 128; c++) {
        if (counts[c] > 0) {
            counts[c] -= 1;
            half[depth] = c;
            build(counts, half, depth + 1, half_len, middle, buf, acc);
            counts[c] += 1;
        }
    }
}

int main(void) {
    long pairs = 8, rounds = 44;
    long *buf = malloc(64 * sizeof(long));
    long *half = malloc(64 * sizeof(long));
    long sink = 0;
    for (long r = 0; r < rounds; r++) {
        long *counts = malloc(128 * sizeof(long));
        memset(counts, 0, 128 * sizeof(long));
        for (long p = 0; p < pairs; p++) counts[97 + p] = 2;
        counts[97 + r % pairs] += 1;

        long middle = -1, half_len = 0;
        for (long c = 0; c < 128; c++) {
            if (counts[c] % 2 == 1) middle = c;
            counts[c] /= 2;
            half_len += counts[c];
        }

        long acc = 0;
        build(counts, half, 0, half_len, middle, buf, &acc);
        sink = (sink * 131 + acc) % 1000000007L;
        free(counts);
    }
    printf("%ld\n", sink);
    free(buf); free(half);
    return 0;
}
