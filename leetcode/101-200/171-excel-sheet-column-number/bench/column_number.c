/* LeetCode #171 bench harness — C calibration point (clang -O3, single-thread).
 *
 * Horner-fold bijective base-26 parse — same canonical algorithm as the Kara
 * mirror. Compute-bound. A LEN=50000 distinct-title corpus (built once via
 * to_title, too many to tabulate) parsed round-robin keeps the parse from being
 * folded. Sink sums the parsed column numbers across K_ITERS.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LEN 50000L
#define K_ITERS 100000000L

static const char LETTERS[26] = {
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z'};

/* Render the bijective base-26 title of num into a freshly malloc'd string. */
static char *to_title(long num) {
    char tmp[16];
    int len = 0;
    while (num > 0) {
        num -= 1;
        tmp[len++] = LETTERS[num % 26];
        num /= 26;
    }
    char *out = malloc((size_t)len + 1);
    for (int i = 0; i < len; i++) {
        out[i] = tmp[len - 1 - i];
    }
    out[len] = '\0';
    return out;
}

static long to_number(const char *title) {
    long n = 0;
    for (const char *p = title; *p; p++) {
        n = n * 26 + (long)(*p - 'A') + 1;
    }
    return n;
}

int main(void) {
    char **corpus = malloc((size_t)LEN * sizeof(char *));
    for (long i = 0; i < LEN; i++) {
        corpus[i] = to_title(i + 1);
    }
    long sum = 0;
    for (long k = 0; k < K_ITERS; k++) {
        long idx = k % LEN;
        sum += to_number(corpus[idx]);
    }
    printf("%ld\n", sum);
    for (long i = 0; i < LEN; i++) {
        free(corpus[i]);
    }
    free(corpus);
    return 0;
}
