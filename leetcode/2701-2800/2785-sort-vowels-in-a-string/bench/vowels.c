// LeetCode #2785: Sort Vowels in a String -- the bench in C: the ★ arm
// over 20 strings of 10^5 letters from all 52, all drawn first, then each
// answered 10 times; the vowels sorted by `qsort`, the answer a fresh
// buffer.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 20
#define N 100000

static int64_t seed = 2785;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int is_vowel(char c) {
    switch (c) {
    case 'a': case 'e': case 'i': case 'o': case 'u':
    case 'A': case 'E': case 'I': case 'O': case 'U':
        return 1;
    }
    return 0;
}

static int cmp(const void *a, const void *b) {
    return *(const char *)a - *(const char *)b;
}

static char *sort_vowels(const char *s, int64_t n) {
    char *vowels = malloc(n);
    int64_t m = 0;
    for (int64_t i = 0; i < n; i++)
        if (is_vowel(s[i])) vowels[m++] = s[i];
    qsort(vowels, m, 1, cmp);
    char *out = malloc(n);
    int64_t next = 0;
    for (int64_t i = 0; i < n; i++) out[i] = is_vowel(s[i]) ? vowels[next++] : s[i];
    free(vowels);
    return out;
}

static char cases[COUNT][N];

int main(void) {
    int rounds = 10;
    const char *every = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for (int c = 0; c < COUNT; c++)
        for (int64_t i = 0; i < N; i++) cases[c][i] = every[next_random() % 52];
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            char *t = sort_vowels(cases[c], N);
            for (int64_t i = 0; i < N; i++) check = (check * 31 + (unsigned char)t[i]) % 1000000007;
            check = (check + r) % 1000000007;
            free(t);
        }
    }
    printf("%d strings of 10^5, %d rounds: checksum %lld\n", COUNT, rounds, (long long)check);
    return 0;
}
