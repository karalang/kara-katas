// Benchmark for #481: C mirror of the ★ arm (the string read while it is
// written); see magical_string.kara. The string is a growable array of
// 64-bit integers, doubled on demand, as the other languages' vectors are.
#include <stdio.h>
#include <stdlib.h>

static long long magical_string(long long n) {
    long long cap = 16, len = 3;
    long long *s = malloc(sizeof(long long) * cap);
    s[0] = 1;
    s[1] = 2;
    s[2] = 2;
    long long read = 2;
    while (len < n) {
        long long next = 3 - s[len - 1];
        for (long long k = 0; k < s[read]; k++) {
            if (len == cap) {
                cap *= 2;
                s = realloc(s, sizeof(long long) * cap);
            }
            s[len++] = next;
        }
        read++;
    }
    long long ones = 0;
    for (long long i = 0; i < n; i++) {
        if (s[i] == 1) {
            ones++;
        }
    }
    free(s);
    return ones;
}

int main(void) {
    long long rounds = 1000, total = 0, checksum = 0;
    for (long long r = 0; r < rounds; r++) {
        long long ones = magical_string(100000 - r);
        total += ones;
        checksum = (checksum * 31 + ones) % 1000000007;
    }
    printf("%lld rounds of n = 99001 to 100000: 1s add up to %lld, checksum %lld\n", rounds, total, checksum);
    return 0;
}
