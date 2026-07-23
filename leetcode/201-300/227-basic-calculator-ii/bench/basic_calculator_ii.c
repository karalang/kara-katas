#include <stdio.h>
#include <stdlib.h>

// ASCII: '+'=43 '-'=45 '*'=42 '/'=47 '0'=48 '9'=57
static long calculate(const long *bytes, long n) {
    long *stack = malloc((n + 1) * sizeof(long));
    long sp = 0;
    long num = 0;
    long op = 43; // '+'
    for (long i = 0; i < n; i++) {
        long b = bytes[i];
        if (b >= 48 && b <= 57) {
            num = num * 10 + (b - 48);
        }
        int is_op = (b == 43 || b == 45 || b == 42 || b == 47);
        if (is_op || i == n - 1) {
            if (op == 43) {
                stack[sp++] = num;
            } else if (op == 45) {
                stack[sp++] = -num;
            } else if (op == 42) {
                long t = sp > 0 ? stack[--sp] : 0;
                stack[sp++] = t * num;
            } else { // '/'
                long t = sp > 0 ? stack[--sp] : 0;
                stack[sp++] = t / num; // truncates toward zero
            }
            op = b;
            num = 0;
        }
    }
    long total = 0;
    for (long k = 0; k < sp; k++) total += stack[k];
    free(stack);
    return total;
}

static void push_number(long *buf, long *len, long num) {
    if (num >= 10) {
        buf[(*len)++] = 48 + num / 10;
        buf[(*len)++] = 48 + num % 10;
    } else {
        buf[(*len)++] = 48 + num;
    }
}

int main(void) {
    long tokens = 200000;
    long passes = 250;
    long modulus = 1000000007;

    long *buf = malloc((tokens * 3 + 8) * sizeof(long));
    long len = 0;
    long state = 12345;

    state = (state * 1103515245L + 12345L) & 2147483647L;
    push_number(buf, &len, (state % 99) + 1);

    int prev_high = 0;
    for (long t = 1; t < tokens; t++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long opsel = prev_high ? (state % 2) : (state % 4);
        if (opsel == 0) {
            buf[len++] = 43;
            prev_high = 0;
        } else if (opsel == 1) {
            buf[len++] = 45;
            prev_high = 0;
        } else if (opsel == 2) {
            buf[len++] = 42;
            prev_high = 1;
        } else {
            buf[len++] = 47;
            prev_high = 1;
        }
        state = (state * 1103515245L + 12345L) & 2147483647L;
        push_number(buf, &len, (state % 99) + 1);
    }

    long n = len;
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        buf[0] = 49 + (p % 9);
        long r = calculate(buf, n);
        sink = ((sink + r) % modulus + modulus) % modulus;
    }
    printf("%ld\n", sink);
    free(buf);
    return 0;
}
