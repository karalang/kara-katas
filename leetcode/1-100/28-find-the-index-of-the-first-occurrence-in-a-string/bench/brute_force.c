/*
 * LeetCode 28 — brute-force sliding-window strStr, C mirror.
 * Algorithmic peer of bench/brute_force.{kara,rs,py}. Same N, M, K,
 * adversarial input, same sink.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t str_str(const uint8_t *haystack, int64_t hn,
                       const uint8_t *needle, int64_t nn) {
    if (nn == 0) {
        return 0;
    }
    if (nn > hn) {
        return -1;
    }
    for (int64_t i = 0; i <= hn - nn; i++) {
        int64_t j = 0;
        while (j < nn && haystack[i + j] == needle[j]) {
            j++;
        }
        if (j == nn) {
            return i;
        }
    }
    return -1;
}

int main(void) {
    const size_t N = 2000000;
    const size_t M = 16;

    uint8_t *haystack = (uint8_t *)malloc(N);
    for (size_t i = 0; i < N; i++) {
        haystack[i] = 'a';
    }
    haystack[N - 1] = 'b';
    uint8_t *needle = (uint8_t *)malloc(M);
    for (size_t i = 0; i < M; i++) {
        needle[i] = 'a';
    }
    needle[M - 1] = 'b';

    int64_t total = 0;
    for (int iter = 0; iter < 10; iter++) {
        total += str_str(haystack, (int64_t)N, needle, (int64_t)M);
    }
    printf("%lld\n", (long long)total);

    free(haystack);
    free(needle);
    return 0;
}
