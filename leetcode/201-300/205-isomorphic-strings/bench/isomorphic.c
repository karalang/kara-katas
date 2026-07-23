#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long len = 600000, w = 200, a = 20011;
    long *s = malloc(len * sizeof(long));
    long *t = malloc(len * sizeof(long));
    long state = 12345;
    for (long i = 0; i < len; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        s[i] = state % a;
    }
    for (long i = 0; i < len; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        t[i] = state % a;
    }

    long *st_val = calloc(a, sizeof(long));
    long *st_ver = malloc(a * sizeof(long));
    long *ts_val = calloc(a, sizeof(long));
    long *ts_ver = malloc(a * sizeof(long));
    for (long z = 0; z < a; z++) {
        st_ver[z] = -1;
        ts_ver[z] = -1;
    }

    long sink = 0;
    long last = len - w + 1;
    for (long start = 0; start < last; start++) {
        long stamp = start;
        int iso = 1;
        long k = 0;
        while (iso && k < w) {
            long ch = s[start + k];
            long dh = t[start + k];
            if (st_ver[ch] != stamp) {
                st_ver[ch] = stamp;
                st_val[ch] = dh;
            } else {
                if (st_val[ch] != dh) iso = 0;
            }
            if (iso) {
                if (ts_ver[dh] != stamp) {
                    ts_ver[dh] = stamp;
                    ts_val[dh] = ch;
                } else {
                    if (ts_val[dh] != ch) iso = 0;
                }
            }
            k++;
        }
        if (iso) sink += 1;
    }
    printf("%ld\n", sink);
    free(s); free(t);
    free(st_val); free(st_ver); free(ts_val); free(ts_ver);
    return 0;
}
