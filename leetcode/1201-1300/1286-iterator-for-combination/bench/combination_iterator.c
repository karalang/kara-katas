// LeetCode #1286 bench, in C: the ★ arm (the masks with k bits, from the
// largest down) over every length of the 15 letters "abcdefghijklmno",
// 1000 rounds, every combination folded into a checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char chars[32];
    int64_t n, k, mask;
} CombinationIterator;

static CombinationIterator make(const char *characters, int64_t k) {
    CombinationIterator it;
    it.n = (int64_t)strlen(characters);
    memcpy(it.chars, characters, it.n);
    it.k = k;
    it.mask = (((int64_t)1 << k) - 1) << (it.n - k);
    return it;
}

// The next combination, written into `out` (a fresh string each call).
static char *next(CombinationIterator *it) {
    char *out = malloc(it->n + 1);
    int64_t len = 0;
    for (int64_t i = 0; i < it->n; i++)
        if ((it->mask >> (it->n - 1 - i)) & 1) out[len++] = it->chars[i];
    out[len] = 0;
    it->mask -= 1;
    while (it->mask > 0 && __builtin_popcountll(it->mask) != it->k) it->mask -= 1;
    return out;
}

static int has_next(const CombinationIterator *it) { return it->mask > 0; }

int main(void) {
    int64_t check = 0;
    for (int64_t round = 0; round < 1000; round++)
        for (int64_t k = 1; k < 16; k++) {
            CombinationIterator it = make("abcdefghijklmno", k);
            while (has_next(&it)) {
                char *s = next(&it);
                for (char *p = s; *p; p++) check = (check * 131 + (unsigned char)*p + round) % 1000000007;
                free(s);
            }
        }
    printf("1000 rounds of every length of 15 letters: checksum %lld\n", (long long)check);
    return 0;
}
