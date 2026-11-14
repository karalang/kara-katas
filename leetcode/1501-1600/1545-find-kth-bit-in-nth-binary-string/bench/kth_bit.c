// LeetCode #1545: Find Kth Bit in Nth Binary String -- bench: the ★ arm (the
// definition's recursion) asked for every place of S_20, two passes. C
// mirror of kth_bit.kara.

#include <stdint.h>
#include <stdio.h>

static char find_kth_bit(int64_t n, int64_t k) {
    if (n == 1) return '0';
    int64_t middle = (int64_t)1 << (n - 1);
    if (k == middle) return '1';
    if (k < middle) return find_kth_bit(n - 1, k);
    return find_kth_bit(n - 1, ((int64_t)1 << n) - k) == '0' ? '1' : '0';
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t check = 0, ones = 0;
    for (int p = 0; p < 2; p++) {
        for (int64_t k = 1; k < 1048576; k++) {
            int64_t bit = find_kth_bit(20, k) == '1' ? 1 : 0;
            ones += bit;
            check = mix(check, bit);
        }
    }
    printf("2 passes over every place of S_20: %lld ones, checksum %lld\n", (long long)ones, (long long)check);
    return 0;
}
