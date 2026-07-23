#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n = 3000, passes = 60, vr = 100000;
    long *val = malloc(n * sizeof(long));
    long *nxt = malloc(n * sizeof(long));
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        val[i] = state % vr;
        nxt[i] = -1;
    }

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long idx = state % n;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        val[idx] = state % vr;

        long head = -1;
        for (long i = 0; i < n; i++) {
            long v = val[i];
            if (head == -1) {
                head = i;
                nxt[i] = -1;
            } else if (val[head] >= v) {
                nxt[i] = head;
                head = i;
            } else {
                long prev = head;
                int scanning = 1;
                while (scanning) {
                    long np = nxt[prev];
                    if (np == -1) {
                        scanning = 0;
                    } else if (val[np] < v) {
                        prev = np;
                    } else {
                        scanning = 0;
                    }
                }
                nxt[i] = nxt[prev];
                nxt[prev] = i;
            }
        }

        long cur = head;
        long pos = 1;
        while (cur != -1) {
            sink += pos * val[cur];
            pos++;
            cur = nxt[cur];
        }
    }
    printf("%ld\n", sink);
    free(val);
    free(nxt);
    return 0;
}
