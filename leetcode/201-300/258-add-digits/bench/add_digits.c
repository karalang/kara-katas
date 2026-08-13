// Benchmark workload for LeetCode #258 — Add Digits (C mirror).
// Mirrors add_digits.kara algorithm-for-algorithm.
#include <stdio.h>

static long add_digits(long num) {
    long n = num;
    while (n >= 10) {
        long sum = 0;
        while (n > 0) { sum += n % 10; n /= 10; }
        n = sum;
    }
    return n;
}

int main(void) {
    long iters = 10000000, state = 258258, sink = 0;
    for (long i = 0; i < iters; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long shift = (state / 65536L) % 33L;
        long v = (state / 8L) * (1L << shift) % 9223372036854775807L;
        sink = (sink + add_digits(v)) % 1000000007L;
    }
    printf("%ld\n", sink);
    return 0;
}
