#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n = 3000, passes = 40000, vrange = 50;
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
        long target = p % vrange;
        for (long r = 0; r < n; r++) {
            nxt[r] = (r + 1 < n) ? r + 1 : -1;
        }
        long head = 0;
        while (head != -1 && val[head] == target) {
            head = nxt[head];
        }
        if (head != -1) {
            long prev = head;
            long cur = nxt[head];
            while (cur != -1) {
                if (val[cur] == target) {
                    nxt[prev] = nxt[cur];
                } else {
                    prev = cur;
                }
                cur = nxt[cur];
            }
        }
        long pass_sum = 0;
        for (long c = head; c != -1; c = nxt[c]) {
            pass_sum += val[c];
        }
        sink += pass_sum;
    }
    printf("%ld\n", sink);
    free(val);
    free(nxt);
    return 0;
}
