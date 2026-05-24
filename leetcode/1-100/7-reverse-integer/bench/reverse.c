/*
 * LeetCode 7 — pop-and-push Reverse Integer, C mirror.
 * Algorithmic peer of bench/reverse.{kara,rs,py}. Same N, K, same
 * LCG-style input fill, same sink formula.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int32_t reverse(int32_t x) {
    int32_t result = 0;
    const int32_t int_max = 2147483647;
    const int32_t int_min = -2147483648;
    const int32_t max_div = int_max / 10;
    const int32_t min_div = int_min / 10;

    while (x != 0) {
        int32_t digit = x % 10;
        if (result > max_div || (result == max_div && digit > 7)) {
            return 0;
        }
        if (result < min_div || (result == min_div && digit < -8)) {
            return 0;
        }
        result = result * 10 + digit;
        x /= 10;
    }
    return result;
}

int main(void) {
    const int64_t n = 1024;
    const int64_t k_iters = 50000000LL;

    int32_t *inputs = (int32_t *)malloc((size_t)n * sizeof(int32_t));
    for (int64_t i = 0; i < n; i++) {
        int64_t raw = i * 2654435769LL + 305419896LL;
        inputs[i] = (int32_t)raw;
    }

    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        size_t idx = (size_t)(k % n);
        sum += (int64_t)reverse(inputs[idx]);
    }
    printf("%lld\n", (long long)sum);

    free(inputs);
    return 0;
}
