#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n = 3000, passes = 40000, vrange = 100;
    long *val = malloc(n * sizeof(long));
    long *nxt = malloc(n * sizeof(long));
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        val[i] = state % vrange;
        nxt[i] = -1;
    }

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long hit = p % n;
        val[hit] = val[hit] + 1;
        for (long r = 0; r < n; r++) {
            nxt[r] = (r + 1 < n) ? r + 1 : -1;
        }
        long prev = -1;
        long cur = 0;
        while (cur != -1) {
            long saved = nxt[cur];
            nxt[cur] = prev;
            prev = cur;
            cur = saved;
        }
        long head = prev;
        long pass_sum = 0;
        long idx = 0;
        for (long c = head; c != -1; c = nxt[c]) {
            pass_sum += (idx + 1) * val[c];
            idx++;
        }
        sink += pass_sum;
    }
    printf("%ld\n", sink);
    free(val);
    free(nxt);
    return 0;
}
