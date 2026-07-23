#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int revisions(const char *v, int len, long *revs) {
    int cnt = 0;
    int i = 0;
    while (i < len) {
        long val = 0;
        while (i < len && v[i] != '.') {
            val = val * 10 + (v[i] - '0');
            i++;
        }
        revs[cnt++] = val;
        i++; // skip the '.'
    }
    return cnt;
}

static int compare_version(const char *a, int la, const char *b, int lb) {
    long ra[8], rb[8];
    int na = revisions(a, la, ra);
    int nb = revisions(b, lb, rb);
    int m = na > nb ? na : nb;
    for (int i = 0; i < m; i++) {
        long x = i < na ? ra[i] : 0;
        long y = i < nb ? rb[i] : 0;
        if (x < y) return -1;
        if (x > y) return 1;
    }
    return 0;
}

int main(void) {
    long m = 4096, passes = 10000000;
    char **pool = malloc(m * sizeof(char *));
    int *plen = malloc(m * sizeof(int));
    long state = 12345;
    for (long k = 0; k < m; k++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long r = 1 + (state % 4);
        char buf[64];
        int off = 0;
        for (long t = 0; t < r; t++) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long rev = state % 1000;
            if (t > 0) buf[off++] = '.';
            off += sprintf(buf + off, "%ld", rev);
        }
        buf[off] = '\0';
        pool[k] = malloc(off + 1);
        memcpy(pool[k], buf, off + 1);
        plen[k] = off;
    }
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long i = state % m;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long j = state % m;
        sink += compare_version(pool[i], plen[i], pool[j], plen[j]) + 1;
    }
    printf("%ld\n", sink);
    for (long k = 0; k < m; k++) free(pool[k]);
    free(pool);
    free(plen);
    return 0;
}
