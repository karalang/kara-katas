/*
 * LeetCode 28 — KMP strStr, C mirror. Same adversarial input as brute_force.c.
 * Algorithmic peer of bench/kmp.{kara,rs,py}.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static void build_lps(const uint8_t *pat, int64_t m, int64_t *lps) {
    lps[0] = 0;
    int64_t len = 0;
    int64_t i = 1;
    while (i < m) {
        if (pat[i] == pat[len]) {
            len++;
            lps[i] = len;
            i++;
        } else if (len > 0) {
            len = lps[len - 1];
        } else {
            lps[i] = 0;
            i++;
        }
    }
}

static int64_t str_str(const uint8_t *haystack, int64_t hn,
                       const uint8_t *needle, int64_t nn) {
    if (nn == 0) {
        return 0;
    }
    if (nn > hn) {
        return -1;
    }
    int64_t *lps = (int64_t *)malloc((size_t)nn * sizeof(int64_t));
    build_lps(needle, nn, lps);
    int64_t i = 0, j = 0, result = -1;
    while (i < hn) {
        if (haystack[i] == needle[j]) {
            i++;
            j++;
            if (j == nn) {
                result = i - nn;
                break;
            }
        } else if (j > 0) {
            j = lps[j - 1];
        } else {
            i++;
        }
    }
    free(lps);
    return result;
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
    for (int iter = 0; iter < 100; iter++) {
        total += str_str(haystack, (int64_t)N, needle, (int64_t)M);
    }
    printf("%lld\n", (long long)total);

    free(haystack);
    free(needle);
    return 0;
}
