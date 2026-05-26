/*
 * LeetCode 9 — half-reverse Palindrome Number, C mirror.
 * Algorithmic peer of bench/palindrome.{kara,rs,py}. Same N, K, same
 * LCG fill + every-16th manufactured 8-digit palindrome, same sink.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int is_palindrome(int32_t x) {
    if (x < 0 || (x % 10 == 0 && x != 0)) {
        return 0;
    }
    int32_t reversed = 0;
    while (x > reversed) {
        reversed = reversed * 10 + x % 10;
        x /= 10;
    }
    return (x == reversed) || (x == reversed / 10);
}

static int32_t manufacture_palindrome(int32_t v32) {
    int32_t lo = v32 < 0 ? -v32 : v32;
    int32_t four_raw = lo % 10000;
    int32_t four = four_raw < 1000 ? four_raw + 1000 : four_raw;
    int32_t d0 = four % 10;
    int32_t d1 = (four / 10) % 10;
    int32_t d2 = (four / 100) % 10;
    int32_t d3 = (four / 1000) % 10;
    int32_t rev = d0 * 1000 + d1 * 100 + d2 * 10 + d3;
    return four * 10000 + rev;
}

int main(void) {
    const int64_t n = 1024;
    const int64_t k_iters = 50000000LL;

    int32_t *inputs = (int32_t *)malloc((size_t)n * sizeof(int32_t));
    for (int64_t i = 0; i < n; i++) {
        int64_t raw = i * 2654435769LL + 305419896LL;
        int32_t v32 = (int32_t)raw;
        inputs[i] = (i % 16 == 0) ? manufacture_palindrome(v32) : v32;
    }

    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        size_t idx = (size_t)(k % n);
        sum += is_palindrome(inputs[idx]) ? 1 : 0;
    }
    printf("%lld\n", (long long)sum);

    free(inputs);
    return 0;
}
