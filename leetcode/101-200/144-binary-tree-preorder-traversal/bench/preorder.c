#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n = 50000, passes = 400;

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

    long *stack = malloc(n * sizeof(long));
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long idx = p % n;
        val[idx] += 1;

        long sp = 0;
        stack[sp++] = 0;
        long pos = 0, acc = 0;
        while (sp > 0) {
            long node = stack[--sp];
            acc += val[node] * (pos + 1);
            pos++;
            long r = right[node], l = left[node];
            if (r >= 0) stack[sp++] = r;
            if (l >= 0) stack[sp++] = l;
        }
        sink += acc;
    }
    printf("%ld\n", sink);
    free(val); free(left); free(right); free(stack);
    return 0;
}
