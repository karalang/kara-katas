// LeetCode #1119: Remove Vowels from a String -- the bench in C, the ★
// arm's filter over the same 64 texts and 2000 rounds. Each text is
// copied into its own `malloc`, as a `String` is built in the other
// languages, and each answer is its own `malloc`.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static char *remove_vowels(const char *s, size_t n, size_t *len) {
    char *out = malloc(n + 1);
    size_t k = 0;
    for (size_t i = 0; i < n; i++) {
        switch (s[i]) {
        case 'a': case 'e': case 'i': case 'o': case 'u': break;
        default: out[k++] = s[i];
        }
    }
    out[k] = 0;
    *len = k;
    return out;
}

static int64_t seed = 1119;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    static char texts[64][1000];
    for (int j = 0; j < 64; j++)
        for (int i = 0; i < 1000; i++) texts[j][i] = letters[next_random() % 26];
    int64_t kept = 0, check = 0;
    for (int64_t round = 0; round < 2000; round++) {
        for (int64_t j = 0; j < 64; j++) {
            int64_t at = (round * 7919 + j * 104729) % 1000;
            texts[j][at] = letters[(round + j) % 26];
            char *s = malloc(1001);
            memcpy(s, texts[j], 1000);
            s[1000] = 0;
            size_t len;
            char *r = remove_vowels(s, 1000, &len);
            free(s);
            kept += (int64_t)len;
            check = (check * 31 + (int64_t)len + (len > 0 ? (unsigned char)r[0] : 0)) % 1000000007;
            free(r);
        }
    }
    printf("2000 rounds over 64 texts of 1000 letters: %lld letters kept, checksum %lld\n", (long long)kept, (long long)check);
    return 0;
}
