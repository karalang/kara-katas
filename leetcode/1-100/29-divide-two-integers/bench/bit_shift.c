/*
 * LeetCode 29 — bit-shift long division, C mirror.
 * Algorithmic peer of bench/bit_shift.{kara,rs,py}. Same N, LCG inputs,
 * same truncating bit-shift divide, same sink formula.
 */
#include <stdio.h>
#include <stdint.h>

static int64_t divide(int64_t dividend, int64_t divisor) {
    const int64_t int_max = 2147483647;
    const int64_t int_min = -2147483648;
    if (dividend == int_min && divisor == -1) {
        return int_max;
    }
    int negative = (dividend < 0) != (divisor < 0);
    int64_t a = dividend < 0 ? -dividend : dividend;
    int64_t b = divisor < 0 ? -divisor : divisor;
    int64_t result = 0;
    while (a >= b) {
        int64_t temp = b;
        int64_t multiple = 1;
        while (a >= (temp << 1)) {
            temp <<= 1;
            multiple <<= 1;
        }
        a -= temp;
        result += multiple;
    }
    return negative ? -result : result;
}

int main(void) {
    const int64_t n = 5000000;
    int64_t state = 1;
    int64_t sum = 0;
    for (int64_t i = 0; i < n; i++) {
        state = (state * 1103515245 + 12345) % 2147483648;
        int64_t dividend = state - 1073741824;
        state = (state * 1103515245 + 12345) % 2147483648;
        int64_t divisor = (state % 2000) - 1000;
        if (divisor == 0) divisor = 1;
        sum += divide(dividend, divisor);
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
