// LeetCode #1359 bench -- C: the product of i (2i - 1) for i from 1 to n,
// modulo 10^9 + 7.
#include <stdint.h>
#include <stdio.h>

#define MOD 1000000007LL

static int32_t count_orders(int32_t n) {
    int64_t count = 1;
    for (int64_t i = 1; i <= n; i++) count = count * i % MOD * (2 * i - 1) % MOD;
    return (int32_t)count;
}

int main(void) {
    // 3 * 10^5 questions, each n from 1 to 500 drawn from the checksum so
    // far, every answer folded into it
    int64_t check = 0;
    for (int64_t r = 0; r < 300000; r++) {
        int32_t n = (int32_t)(1 + check % 500);
        check = (check * 31 + count_orders(n) + r) % MOD;
    }
    printf("300000 questions: checksum %lld\n", (long long)check);
    return 0;
}
