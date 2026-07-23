#include <stdio.h>
#include <stdlib.h>

static long scan(const long *bases, long *stamp, long *cnt, long n, long pass) {
    long mask = 1048575; /* 2^20 - 1 */
    long hash = 0;
    long dups = 0;
    for (long i = 0; i < n; i++) {
        hash = ((hash << 2) | bases[i]) & mask;
        if (i >= 9) {
            long key = hash;
            if (stamp[key] != pass) {
                stamp[key] = pass;
                cnt[key] = 0;
            }
            long c = cnt[key] + 1;
            cnt[key] = c;
            if (c == 2) {
                dups++;
            }
        }
    }
    return dups;
}

int main(void) {
    long n = 1000000;
    long passes = 30;
    long tablesize = 1048576; /* 2^20 */

    long *bases = malloc((size_t)n * sizeof(long));
    long state = 12345;
    for (long b = 0; b < n; b++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        bases[b] = (state >> 16) % 4;
    }

    long *stamp = malloc((size_t)tablesize * sizeof(long));
    long *cnt = malloc((size_t)tablesize * sizeof(long));
    for (long t = 0; t < tablesize; t++) {
        stamp[t] = -1;
        cnt[t] = 0;
    }

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        long idx = state % n;
        bases[idx] = (state >> 16) % 4;
        sink += scan(bases, stamp, cnt, n, p);
    }
    printf("%ld\n", sink);
    free(bases);
    free(stamp);
    free(cnt);
    return 0;
}
