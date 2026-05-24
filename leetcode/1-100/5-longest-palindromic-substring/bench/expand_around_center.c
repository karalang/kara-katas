/*
 * LeetCode 5 — expand-around-center Longest Palindromic Substring, C mirror.
 * Algorithmic peer of bench/expand_around_center.{kara,rs,py}. Same input:
 * 5000 'a' chars, K=10, sink = sum of (best_start + best_len) per call.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static void expand(const char *s, int64_t n, int64_t lo0, int64_t hi0,
                   int64_t *out_lo, int64_t *out_len) {
    int64_t lo = lo0;
    int64_t hi = hi0;
    while (lo >= 0 && hi < n && s[lo] == s[hi]) {
        lo--;
        hi++;
    }
    *out_lo = lo + 1;
    *out_len = hi - lo - 1;
}

static void longest_palindrome(const char *s, int64_t n,
                               int64_t *best_start, int64_t *best_len) {
    int64_t bs = 0;
    int64_t bl = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t start, length;
        expand(s, n, i, i, &start, &length);
        if (length > bl) {
            bs = start;
            bl = length;
        }
        expand(s, n, i, i + 1, &start, &length);
        if (length > bl) {
            bs = start;
            bl = length;
        }
    }
    *best_start = bs;
    *best_len = bl;
}

int main(void) {
    const int64_t n = 5000;
    char *data = (char *)malloc((size_t)n + 1);
    memset(data, 'a', (size_t)n);
    data[n] = '\0';

    int64_t sum = 0;
    for (int k = 0; k < 10; k++) {
        int64_t start, length;
        longest_palindrome(data, n, &start, &length);
        sum += start + length;
    }
    printf("%lld\n", (long long)sum);
    free(data);
    return 0;
}
