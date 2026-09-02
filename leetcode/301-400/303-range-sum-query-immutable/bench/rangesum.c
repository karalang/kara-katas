/* Benchmark mirror of rangesum.kara — LeetCode #303, O(1) prefix-sum query.
 * Same LCG, same query list, same sink. */
#include <stdio.h>
#include <stdlib.h>

#define N        65536
#define NQUERIES 200000
#define PASSES   1800

static long long prefix[N + 1];
static long qs[NQUERIES * 2];

int main(void) {
    long long state = 20303;

    prefix[0] = 0;
    for (int i = 0; i < N; i++) {
        state = (state * 1103515245LL + 12345LL) & 0x7fffffffLL;
        long long v = (state / 65536) % 2001 - 1000;
        prefix[i + 1] = prefix[i] + v;
    }

    for (int q = 0; q < NQUERIES; q++) {
        state = (state * 1103515245LL + 12345LL) & 0x7fffffffLL;
        long x = (long)((state / 65536) % N);
        state = (state * 1103515245LL + 12345LL) & 0x7fffffffLL;
        long y = (long)((state / 65536) % N);
        if (x <= y) { qs[q * 2] = x; qs[q * 2 + 1] = y; }
        else        { qs[q * 2] = y; qs[q * 2 + 1] = x; }
    }

    long long checksum = 0;
    for (int p = 0; p < PASSES; p++) {
        for (int k = 0; k < NQUERIES; k++) {
            long long v = prefix[qs[k * 2 + 1] + 1] - prefix[qs[k * 2]];
            checksum = (checksum + v) & 0x3FFFFFFF;
        }
    }

    printf("checksum %lld\n", checksum);
    return 0;
}
