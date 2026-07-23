#include <stdio.h>
#include <stdlib.h>

// ASCII: '+'=43 '-'=45 '('=40 ')'=41 '0'=48 '9'=57
static long calculate(const long *bytes, long n, long *stack) {
    long result = 0;
    long sign = 1;
    long sp = 0;
    long i = 0;
    while (i < n) {
        long b = bytes[i];
        if (b >= 48 && b <= 57) {
            long num = 0;
            while (i < n && bytes[i] >= 48 && bytes[i] <= 57) {
                num = num * 10 + (bytes[i] - 48);
                i++;
            }
            result = result + sign * num;
        } else if (b == 43) {
            sign = 1;
            i++;
        } else if (b == 45) {
            sign = -1;
            i++;
        } else if (b == 40) {
            stack[sp++] = result;
            stack[sp++] = sign;
            result = 0;
            sign = 1;
            i++;
        } else if (b == 41) {
            long saved_sign = sp > 0 ? stack[--sp] : 1;
            long saved_result = sp > 0 ? stack[--sp] : 0;
            result = saved_result + saved_sign * result;
            i++;
        } else {
            i++;
        }
    }
    return result;
}

static void push_number(long *buf, long *len, long num) {
    if (num >= 100) {
        buf[(*len)++] = 48 + num / 100;
        buf[(*len)++] = 48 + (num / 10) % 10;
        buf[(*len)++] = 48 + num % 10;
    } else if (num >= 10) {
        buf[(*len)++] = 48 + num / 10;
        buf[(*len)++] = 48 + num % 10;
    } else {
        buf[(*len)++] = 48 + num;
    }
}

int main(void) {
    long nums = 250000;
    long passes = 80;
    long max_depth = 16;
    long modulus = 1000000007;

    long *buf = malloc((nums * 6 + 64) * sizeof(long));
    long len = 0;
    long state = 12345;
    long depth = 0;

    state = (state * 1103515245L + 12345L) & 2147483647L;
    push_number(buf, &len, state % 1000);

    for (long t = 1; t < nums; t++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        if (state % 2 == 0) buf[len++] = 43; else buf[len++] = 45;

        state = (state * 1103515245L + 12345L) & 2147483647L;
        long opens = state % 3;
        int opened_here = 0;
        for (long o = 0; o < opens; o++) {
            if (depth < max_depth) {
                buf[len++] = 40;
                depth++;
                opened_here = 1;
            }
        }

        if (opened_here) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            if (state % 4 == 0) buf[len++] = 45;
        }

        state = (state * 1103515245L + 12345L) & 2147483647L;
        push_number(buf, &len, state % 1000);

        state = (state * 1103515245L + 12345L) & 2147483647L;
        long closes = state % 3;
        for (long c = 0; c < closes; c++) {
            if (depth > 0) {
                buf[len++] = 41;
                depth--;
            }
        }
    }
    while (depth > 0) {
        buf[len++] = 41;
        depth--;
    }

    long n = len;
    long *stack = malloc((n + 2) * sizeof(long));
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        buf[0] = 48 + (p % 10);
        long r = calculate(buf, n, stack);
        sink = ((sink + r) % modulus + modulus) % modulus;
    }
    printf("%ld\n", sink);
    free(buf);
    free(stack);
    return 0;
}
