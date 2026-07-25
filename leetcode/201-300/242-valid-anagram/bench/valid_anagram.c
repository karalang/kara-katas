/* Benchmark harness for LeetCode #242 — Valid Anagram.
 * Mirrors valid_anagram.kara algorithm-for-algorithm.
 *
 * No hash map here — the kata is a fixed 26-slot frequency array, so every
 * language runs the same structure. That makes this one of the cleaner
 * like-for-like comparisons in the corpus: no data-structure divergence to
 * caveat, unlike #290/#291 where C's map differed from the others.
 */

#include <stdio.h>
#include <string.h>

#define NP 8
#define SL 20000
#define ITERS 8000

static unsigned char esses[NP][SL];
static unsigned char tees[NP][SL];

static int is_anagram(const unsigned char *s, const unsigned char *t, long long len) {
    long long count[26];
    memset(count, 0, sizeof(count));
    for (long long i = 0; i < len; i++) {
        count[s[i] - 97] += 1;
        count[t[i] - 97] -= 1;
    }
    for (int j = 0; j < 26; j++) {
        if (count[j] != 0) {
            return 0;
        }
    }
    return 1;
}

int main(void) {
    for (long long j = 0; j < NP; j++) {
        for (long long k = 0; k < SL; k++) {
            esses[j][k] = (unsigned char)(97 + ((k * 7 + j) % 26));
        }
        long long w = 0;
        for (long long m = SL - 1; m >= 0; m--) {
            long long b = esses[j][m];
            if (j % 2 == 1 && m == 0) {
                b = 97 + ((b - 97 + 1) % 26);
            }
            tees[j][w++] = (unsigned char)b;
        }
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        if (is_anagram(esses[idx], tees[idx], SL)) {
            sink += it + 1;
        } else {
            sink += 1;
        }
    }
    printf("%lld\n", sink);
    return 0;
}
