// Benchmark workload for LeetCode #250 — Count Univalue Subtrees (C mirror).
// Mirrors count_univalue.kara algorithm-for-algorithm: same LCG, same complete
// level-order tree, same descending post-order scan over the node pool.
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long nodes_n = 2000000;
    long passes = 40;
    long alphabet = 3;

    long *val = malloc(nodes_n * sizeof(long));
    long state = 250250;
    for (long i = 0; i < nodes_n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        val[i] = (state / 65536L) % alphabet;
    }

    unsigned char *uni = calloc(nodes_n, 1);

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long total = 0;
        for (long j = nodes_n - 1; j >= 0; j--) {
            long left = 2 * j + 1;
            long right = 2 * j + 2;
            int ok = 1;
            if (left < nodes_n) {
                if (!uni[left] || val[left] != val[j]) ok = 0;
            }
            if (right < nodes_n) {
                if (!uni[right] || val[right] != val[j]) ok = 0;
            }
            uni[j] = (unsigned char)ok;
            if (ok) total++;
        }
        sink = (sink + total) % 1000000007L;
    }
    printf("%ld\n", sink);

    free(val);
    free(uni);
    return 0;
}
