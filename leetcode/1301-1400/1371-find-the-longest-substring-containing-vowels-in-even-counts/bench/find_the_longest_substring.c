// LeetCode #1371 bench -- C: each vowel's count kept as a parity bit, and
// the answer the furthest apart two prefixes with the same bits are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LEN 500000

static int32_t find_the_longest_substring(const char *s, size_t n) {
    int64_t first[32];
    for (int k = 0; k < 32; k++) first[k] = -2;
    first[0] = -1;
    int bits = 0;
    int64_t best = 0;
    for (size_t i = 0; i < n; i++) {
        switch (s[i]) {
        case 'a': bits ^= 1; break;
        case 'e': bits ^= 2; break;
        case 'i': bits ^= 4; break;
        case 'o': bits ^= 8; break;
        case 'u': bits ^= 16; break;
        default: break;
        }
        if (first[bits] == -2) {
            first[bits] = (int64_t)i;
        } else if ((int64_t)i - first[bits] > best) {
            best = (int64_t)i - first[bits];
        }
    }
    return (int32_t)best;
}

static int64_t seed = 1371;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    // 4 strings of 5 * 10^5 letters, the constraints' most, drawn from
    // "aeioubcxyz", built once; then 80 rounds, each changing one letter
    // of one string to a copy, both drawn from the checksum so far, and
    // finding that string's longest substring
    const char *pool = "aeioubcxyz";
    char *strings[4];
    for (int k = 0; k < 4; k++) {
        strings[k] = malloc(LEN);
        for (int j = 0; j < LEN; j++) strings[k][j] = pool[next_random() % 10];
    }
    int64_t check = 0;
    for (int64_t r = 0; r < 80; r++) {
        int64_t i = check % 4;
        int64_t at = (check / 4) % LEN;
        char *copy = malloc(LEN);
        memcpy(copy, strings[i], LEN);
        copy[at] = pool[(check / 2000000) % 10];
        free(strings[i]);
        strings[i] = copy;
        int64_t got = find_the_longest_substring(strings[i], LEN);
        check = (check * 31 + got + r) % 1000000007;
    }
    printf("80 rounds over 4 strings of 500000 letters: checksum %lld\n", (long long)check);
    for (int k = 0; k < 4; k++) free(strings[k]);
    return 0;
}
