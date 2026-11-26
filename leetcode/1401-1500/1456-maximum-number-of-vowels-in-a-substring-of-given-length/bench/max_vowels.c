// LeetCode #1456 bench mirror: a window of k letters slid along the
// string, its vowels counted as a letter comes in and another goes out.
// The letters are copied out as 32-bit characters, as the ★ arm collects
// its chars, and each tested by `strchr` on "aeiou".
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int is_vowel(int32_t c) { return strchr("aeiou", c) != NULL; }

static int32_t max_vowels(const char *s, int64_t n, int32_t k) {
    int32_t *letters = malloc(n * sizeof(int32_t));
    for (int64_t i = 0; i < n; i++) letters[i] = (unsigned char)s[i];
    int32_t count = 0;
    for (int64_t i = 0; i < k; i++)
        if (is_vowel(letters[i])) count++;
    int32_t best = count;
    for (int64_t i = k; i < n; i++) {
        if (is_vowel(letters[i])) count++;
        if (is_vowel(letters[i - k])) count--;
        if (count > best) best = count;
    }
    free(letters);
    return best;
}

static char texts[200][100001];

int main(void) {
    // 200 strings of 10^5 letters, a vowel one time in 3, drawn once, each
    // asked for windows of 1 to 10^5 letters 5 times, the answers folded to
    // a checksum
    int64_t seed = 1456;
    const char *vowels = "aeiou", *others = "bcdfghjklmnpqrstvwxyz";
    for (int t = 0; t < 200; t++) {
        for (int i = 0; i < 100000; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            int odd = seed / 65536 % 3 == 0;
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            int64_t pick = seed / 65536;
            texts[t][i] = odd ? vowels[pick % 5] : others[pick % 21];
        }
        texts[t][100000] = 0;
    }
    int64_t check = 0;
    for (int r = 0; r < 5; r++)
        for (int t = 0; t < 200; t++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            int64_t k = 1 + seed / 65536 % 100000;
            check = (check * 131 + max_vowels(texts[t], 100000, (int32_t)k)) % 1000000007;
        }
    printf("1000 windows of 10^5 letters: checksum %lld\n", (long long)check);
    return 0;
}
