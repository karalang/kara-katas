#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n = 50000, passes = 250;

    long *val   = malloc(n * sizeof(long));
    long *left  = malloc(n * sizeof(long));
    long *right = malloc(n * sizeof(long));

    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        val[i] = state >> 16;
        left[i] = -1;
        right[i] = -1;
    }

    for (long i = 1; i < n; i++) {
        long cur = 0;
        int placed = 0;
        while (!placed) {
            if (val[i] < val[cur]) {
                if (left[cur] < 0) { left[cur] = i; placed = 1; }
                else cur = left[cur];
            } else {
                if (right[cur] < 0) { right[cur] = i; placed = 1; }
                else cur = right[cur];
            }
        }
    }

    long *s1 = malloc(n * sizeof(long));
    long *s2 = malloc(n * sizeof(long));
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long idx = p % n;
        val[idx] += 1;

        long s1p = 0;
        s1[s1p++] = 0;
        long s2p = 0;
        while (s1p > 0) {
            long node = s1[--s1p];
            s2[s2p++] = node;
            long l = left[node], r = right[node];
            if (l >= 0) s1[s1p++] = l;
            if (r >= 0) s1[s1p++] = r;
        }
        long pos = 0, acc = 0;
        while (s2p > 0) {
            long node = s2[--s2p];
            acc += val[node] * (pos + 1);
            pos++;
        }
        sink += acc;
    }
    printf("%ld\n", sink);
    free(val); free(left); free(right); free(s1); free(s2);
    return 0;
}
