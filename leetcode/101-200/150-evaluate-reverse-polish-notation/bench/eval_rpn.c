#include <stdio.h>
#include <stdlib.h>

static long eval_rpn(const long *tok, long t, long *stk, long modp) {
    long sp = 0;
    for (long i = 0; i < t; i++) {
        long x = tok[i];
        if (x >= 0) {
            stk[sp++] = x;
        } else {
            long op = -x - 1;
            long b = stk[--sp];
            long a = stk[--sp];
            long r;
            if (op == 0) r = a + b;
            else if (op == 1) r = a - b;
            else if (op == 2) r = a * b;
            else r = a / b;
            r = ((r % modp) + modp) % modp;
            stk[sp++] = r;
        }
    }
    return stk[0];
}

int main(void) {
    long m = 100000, punches = 700, modp = 1000000007L, opr = 1000;
    long cap = 2 * m + 1;
    long *tok = malloc(cap * sizeof(long));
    long tn = 0;
    long state = 12345;

    state = (state * 1103515245L + 12345L) & 2147483647L;
    tok[tn++] = state % opr + 1;
    state = (state * 1103515245L + 12345L) & 2147483647L;
    tok[tn++] = state % opr + 1;
    state = (state * 1103515245L + 12345L) & 2147483647L;
    tok[tn++] = -(state % 4) - 1;

    for (long k = 2; k <= m; k++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        tok[tn++] = state % opr + 1;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        tok[tn++] = -(state % 4) - 1;
    }

    long stk[4] = {0, 0, 0, 0};

    long sink = 0;
    for (long pn = 0; pn < punches; pn++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long r = state % (m + 1);
        long tokpos = (r == 0) ? 0 : 2 * r - 1;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        tok[tokpos] = state % opr + 1;
        long res = eval_rpn(tok, tn, stk, modp);
        sink = (sink + res) % modp;
    }
    printf("%ld\n", sink);
    free(tok);
    return 0;
}
