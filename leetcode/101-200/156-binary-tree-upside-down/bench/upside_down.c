#include <stdio.h>
#include <stdlib.h>

static long flip(long *left, long *right, long root) {
    long cur = root;
    long prev = -1;
    long prev_right = -1;
    while (cur != -1) {
        long next = left[cur];
        left[cur] = prev_right;
        prev_right = right[cur];
        right[cur] = prev;
        prev = cur;
        cur = next;
    }
    return prev;
}

int main(void) {
    long l = 50000;
    long n = 2 * l;
    long passes = 1100;

    long *val = malloc((size_t)n * sizeof(long));
    long state = 12345;
    for (long c = 0; c < n; c++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        val[c] = state;
    }

    long *left = malloc((size_t)n * sizeof(long));
    long *right = malloc((size_t)n * sizeof(long));
    for (long z = 0; z < n; z++) {
        left[z] = -1;
        right[z] = -1;
    }

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        for (long i = 0; i < l; i++) {
            left[i] = (i < l - 1) ? (i + 1) : -1;
            right[i] = l + i;
        }
        long pp = p % l;
        right[pp] = l + ((p * 7 + 3) % l);

        long new_root = flip(left, right, 0);

        long chk = 0;
        for (long j = 0; j < n; j++) {
            chk = (chk * 1103515245 + val[j] * 3 + left[j] + 2 + right[j] + 5) & 2147483647;
        }
        chk = (chk * 1103515245 + new_root + 1) & 2147483647;
        sink = (sink + chk) & 2147483647;
    }
    printf("%ld\n", sink);
    return 0;
}
