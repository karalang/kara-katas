// LeetCode #1837: Sum of Digits in Base K -- the bench in C: the ★ arm over
// 2 * 10^7 calls, each `n` from 1 to 100 and base from 2 to 10 drawn from the
// checksum so far.
#include <stdint.h>
#include <stdio.h>

static int64_t sum_base(int64_t n, int64_t k) {
    int64_t left = n, sum = 0;
    while (left > 0) {
        sum += left % k;
        left /= k;
    }
    return sum;
}

int main(void) {
    int64_t check = 0;
    for (int64_t call = 0; call < 20000000; call++) {
        int64_t n = 1 + (check + call) % 100;
        int64_t k = 2 + (check / 100 + call) % 9;
        check = (check * 31 + sum_base(n, k)) % 1000000007;
    }
    printf("20000000 calls: checksum %lld\n", (long long)check);
    return 0;
}
