// Benchmark workload for LeetCode #345 — C mirror of reverse_vowels.kara.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LEN 200000
#define PUNCHES 1000
#define MODULUS 1073741789LL

/* A Kāra `char` is one code point; uint32_t holds the same values. */
static bool is_vowel(uint32_t c) {
    switch (c) {
    case 'a': case 'e': case 'i': case 'o': case 'u':
    case 'A': case 'E': case 'I': case 'O': case 'U':
        return true;
    default:
        return false;
    }
}

static void reverse_vowels(uint32_t *cs, int64_t n) {
    int64_t i = 0;
    int64_t j = n - 1;
    while (i < j) {
        if (!is_vowel(cs[i])) {
            i++;
        } else if (!is_vowel(cs[j])) {
            j--;
        } else {
            uint32_t t = cs[i];
            cs[i] = cs[j];
            cs[j] = t;
            i++;
            j--;
        }
    }
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static uint32_t letter(int64_t k) {
    if (k < 26) {
        return (uint32_t)(97 + k);
    }
    return (uint32_t)(65 + k - 26);
}

int main(void) {
    int64_t seed = 345;
    uint32_t *s = malloc(sizeof(uint32_t) * LEN);
    for (int64_t i = 0; i < LEN; i++) {
        s[i] = letter(next(&seed) % 32);
    }
    int64_t sink = 0;
    for (int64_t p = 0; p < PUNCHES; p++) {
        /* Two draws, in order: C leaves the order of `next(seed) * 32768 +
           next(seed)` unspecified, so name them. */
        int64_t x = next(&seed);
        int64_t y = next(&seed);
        int64_t pos = (x * 32768 + y) % LEN;
        s[pos] = letter(next(&seed) % 32);
        reverse_vowels(s, LEN);
        int64_t u = next(&seed);
        int64_t v = next(&seed);
        int64_t at = (u * 32768 + v) % LEN;
        sink = (sink * 31 + (int64_t)s[at]) % MODULUS;
    }
    printf("sink %lld\n", (long long)sink);
    free(s);
    return 0;
}
