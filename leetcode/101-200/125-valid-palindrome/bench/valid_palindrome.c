/* LeetCode #125 bench harness — C calibration point (clang -O3, single-thread).
 *
 * Same allocating filter-then-compare as the Kara mirror: each pass mallocs a
 * normalized buffer (alnum, lowercased) then checks symmetry. Sink = ITERS. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ITERS 3000000
#define REPEAT 8
#define BASE "A man, a plan, a canal: Panama"

static int is_alnum(unsigned char b) {
    return (b >= '0' && b <= '9') || (b >= 'a' && b <= 'z') || (b >= 'A' && b <= 'Z');
}

static int is_palindrome(const unsigned char *s, long n) {
    unsigned char *clean = malloc((size_t)(n > 0 ? n : 1));
    long m = 0;
    for (long i = 0; i < n; i++) {
        unsigned char b = s[i];
        if (is_alnum(b)) {
            clean[m++] = (b >= 'A' && b <= 'Z') ? (unsigned char)(b + 32) : b;
        }
    }
    int ok = 1;
    long lo = 0, hi = m - 1;
    while (lo < hi) {
        if (clean[lo] != clean[hi]) { ok = 0; break; }
        lo++;
        hi--;
    }
    free(clean);
    return ok;
}

int main(void) {
    long base_len = (long)strlen(BASE);
    long n = base_len * REPEAT;
    unsigned char *input = malloc((size_t)n);
    for (int r = 0; r < REPEAT; r++) {
        memcpy(input + (long)r * base_len, BASE, (size_t)base_len);
    }
    long sum = 0;
    for (int it = 0; it < ITERS; it++) {
        sum += is_palindrome(input, n);
    }
    printf("%ld\n", sum);
    free(input);
    return 0;
}
