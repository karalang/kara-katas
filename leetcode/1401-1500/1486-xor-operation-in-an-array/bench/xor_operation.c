// LeetCode #1486: XOR Operation in an Array -- bench, the C twin of
// xor_operation.kara.
#include <stdint.h>
#include <stdio.h>

static int32_t xor_operation(int32_t n, int32_t start) {
    int32_t x = 0;
    for (int32_t i = 0; i < n; i++) x ^= start + 2 * i;
    return x;
}

int main(void) {
    int64_t check = 0;
    for (int64_t q = 0; q < 2000000; q++) {
        int32_t n = (int32_t)(1 + (check + q) % 1000);
        int32_t start = (int32_t)((check / 7 + q * 13) % 1001);
        check = (check * 31 + xor_operation(n, start)) % 1000000007;
    }
    printf("2000000 calls: checksum %lld\n", (long long)check);
    return 0;
}
