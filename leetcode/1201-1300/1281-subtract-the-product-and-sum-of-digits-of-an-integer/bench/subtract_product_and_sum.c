// LeetCode #1281 bench, in C: the ★ arm (the digits by remainders) on
// every n from 1 to 10^5, 2000 rounds, every answer folded into a checksum.
#include <stdio.h>

static long long subtract_product_and_sum(long long n) {
    long long product = 1, sum = 0, rest = n;
    while (rest > 0) {
        long long digit = rest % 10;
        product *= digit;
        sum += digit;
        rest /= 10;
    }
    return product - sum;
}

int main(void) {
    long long check = 0;
    for (long long round = 0; round < 2000; round++)
        for (long long n = 1; n <= 100000; n++)
            check = (check * 131 + subtract_product_and_sum(n) + round + 1000) % 1000000007;
    printf("2000 rounds of 1 to 100000: checksum %lld\n", check);
    return 0;
}
