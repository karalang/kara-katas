// Benchmark for #371 -- mirror of sum.kara. The carry shifts through
// uint64_t, since a left shift of a negative int64_t is undefined in C.
#include <stdint.h>
#include <stdio.h>

static int64_t get_sum(int64_t a, int64_t b) {
    uint64_t x = (uint64_t)a, carry = (uint64_t)b;
    while (carry != 0) {
        uint64_t both = x & carry;
        x = x ^ carry;
        carry = both << 1;
    }
    return (int64_t)x;
}

int main(void) {
    int64_t seed = 371, checksum = 0;
    for (int i = 0; i < 5000000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t a = (seed / 65536) % 2001 - 1000;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t b = (seed / 65536) % 2001 - 1000;
        checksum = (checksum * 31 + get_sum(a, b) + 5000) % 1000000007;
    }
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
