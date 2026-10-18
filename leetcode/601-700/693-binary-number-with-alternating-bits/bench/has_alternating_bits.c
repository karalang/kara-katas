// LeetCode #693: Binary Number with Alternating Bits -- bench program, C mirror of the ★ arm.
#include <stdio.h>

static int has_alternating_bits(long long n) {
    long long x = n ^ (n >> 1);
    return (x & (x + 1)) == 0;
}

int main(void) {
    long long seed = 693;
    long long count = 100000000;
    long long yes = 0, checksum = 0;
    for (long long i = 0; i < count; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        long long n = (1431655765LL >> (seed % 31)) ^ ((seed >> 8) % 4);
        if (n > 0 && has_alternating_bits(n)) {
            yes++;
            checksum = (checksum * 31 + n) % 1000000007;
        }
    }
    printf("%lld numbers: %lld alternate, checksum %lld\n", count, yes, checksum);
    return 0;
}
