#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long len = 200000, passes = 320, modp = 1000000007L, space = 32;
    long *buf = malloc(len * sizeof(long));
    long *ws = malloc(len * sizeof(long));
    long *we = malloc(len * sizeof(long));
    long state = 12345;
    for (long i = 0; i < len; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        if (state % 100 < 15) buf[i] = space;
        else buf[i] = 97 + state % 26;
    }

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long idx = state % len;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        if (state % 100 < 15) buf[idx] = space;
        else buf[idx] = 97 + state % 26;

        long i = 0, m = 0;
        while (i < len) {
            while (i < len && buf[i] == space) i++;
            if (i >= len) break;
            long start = i;
            while (i < len && buf[i] != space) i++;
            ws[m] = start;
            we[m] = i;
            m++;
        }

        for (long k = m - 1; k >= 0; k--) {
            if (k < m - 1) sink = (sink * 131 + space) % modp;
            long e = we[k];
            for (long j = ws[k]; j < e; j++) {
                sink = (sink * 131 + buf[j]) % modp;
            }
        }
    }
    printf("%ld\n", sink);
    free(buf);
    free(ws);
    free(we);
    return 0;
}
