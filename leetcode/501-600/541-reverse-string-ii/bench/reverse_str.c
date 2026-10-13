// Benchmark for #541: C mirror of the ★ arm (two pointers over the
// characters); see reverse_str.kara. The words are ASCII, so each byte is
// one character; the characters are widened to 32 bits as `char` is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *reverse_str(const char *s, int64_t k) {
    int64_t n = (int64_t)strlen(s);
    uint32_t *chars = malloc(n * sizeof(uint32_t));
    for (int64_t i = 0; i < n; i++) chars[i] = (unsigned char)s[i];
    for (int64_t start = 0; start < n; start += 2 * k) {
        int64_t i = start, j = (start + k < n ? start + k : n) - 1;
        while (i < j) {
            uint32_t x = chars[i];
            chars[i] = chars[j];
            chars[j] = x;
            i++;
            j--;
        }
    }
    char *out = malloc(n + 1);
    for (int64_t i = 0; i < n; i++) out[i] = (char)chars[i];
    out[n] = 0;
    free(chars);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 200 random words of 10,000 letters (the problem's longest) built
    // once. Then 100 times over every word is answered with a k from 1
    // to 500 picked by the round and the word, and one letter of the
    // answer, picked the same way, goes into the checksum.
    int64_t words = 200;
    int64_t seed = 541;
    char **all = malloc(words * sizeof(char *));
    for (int64_t t = 0; t < words; t++) {
        all[t] = malloc(10001);
        for (int i = 0; i < 10000; i++) all[t][i] = (char)('a' + next_random(&seed) % 26);
        all[t][10000] = 0;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t r = 0; r < 100; r++) {
        for (int64_t t = 0; t < words; t++) {
            int64_t k = 1 + (r * 37 + t * 11) % 500;
            char *answer = reverse_str(all[t], k);
            int64_t letter = (unsigned char)answer[(r * 7 + t * 13) % 10000];
            total += (int64_t)strlen(answer);
            checksum = (checksum * 31 + letter) % 1000000007;
            free(answer);
        }
    }
    printf("%lld words, 100 times each: %lld letters, checksum %lld\n", (long long)words,
           (long long)total, (long long)checksum);
    return 0;
}
