// LeetCode #44 bench mirror — C, the greedy two-pointer matcher (★).
//
// Mirrors bench/wildcard_matching.kara: one cursor in each of s and p, with star/matched
// scalars for O(1) backtracking. Build s ("abc" repeated) and a multi-star pattern p ONCE,
// then punch one s slot per iteration and fold the boolean into a rolling checksum. Same
// workload + sink as every other mirror.

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int is_match(const unsigned char *s, int64_t n, const unsigned char *p, int64_t m) {
    int64_t i = 0, j = 0, star = -1, matched = 0;
    while (i < n) {
        if (j < m && (p[j] == '?' || p[j] == s[i])) {
            i++;
            j++;
        } else if (j < m && p[j] == '*') {
            star = j;
            matched = i;
            j++;
        } else if (star != -1) {
            matched++;
            i = matched;
            j = star + 1;
        } else {
            return 0;
        }
    }
    while (j < m && p[j] == '*') {
        j++;
    }
    return j == m;
}

int main(void) {
    const int64_t total = 300000;
    const int64_t modulus = 1000000007;
    const int64_t n = 240;

    unsigned char *s = (unsigned char *)malloc((size_t)n);
    for (int64_t a = 0; a < n; a++) {
        s[a] = (unsigned char)('a' + (a % 3));
    }
    const int64_t m = 33; // 8 * "*abc" + "*"
    unsigned char *p = (unsigned char *)malloc((size_t)m);
    int64_t pi = 0;
    for (int64_t g = 0; g < 8; g++) {
        p[pi++] = '*';
        p[pi++] = 'a';
        p[pi++] = 'b';
        p[pi++] = 'c';
    }
    p[pi++] = '*';

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        s[k % n] = (unsigned char)('a' + (k % 4));
        int64_t bit = is_match(s, n, p, m) ? 1 : 0;
        acc = (acc * 131 + bit) % modulus;
    }

    free(s);
    free(p);
    printf("%lld\n", (long long)acc);
    return 0;
}
