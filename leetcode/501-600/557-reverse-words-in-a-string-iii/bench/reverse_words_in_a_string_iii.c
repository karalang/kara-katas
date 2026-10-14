// Benchmark for #557: C mirror of the ★ arm (split, reverse, join); see
// reverse_words_in_a_string_iii.kara. Each word is copied backwards into
// its own malloc'd string, the words are kept in a growing array, and
// they are joined into one fresh string, as the Kāra arm's Vec of
// Strings and `join` are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

typedef struct {
    char *p;
    size_t len;
} Str;

static Str reverse_words(const char *s, size_t n) {
    size_t cap = 16, count = 0, total = 0;
    Str *words = malloc(cap * sizeof(Str));
    size_t start = 0;
    for (;;) {
        size_t end = start;
        while (end < n && s[end] != ' ') end++;
        Str w = {malloc(end - start + 1), end - start};
        for (size_t k = 0; k < w.len; k++) w.p[k] = s[end - 1 - k];
        if (count == cap) words = realloc(words, (cap *= 2) * sizeof(Str));
        words[count++] = w;
        total += w.len;
        if (end >= n) break;
        start = end + 1;
    }
    Str out = {malloc(total + count), total + count - 1};
    size_t at = 0;
    for (size_t k = 0; k < count; k++) {
        if (k > 0) out.p[at++] = ' ';
        memcpy(out.p + at, words[k].p, words[k].len);
        at += words[k].len;
        free(words[k].p);
    }
    free(words);
    return out;
}

int main(void) {
    const int count = 100;
    int64_t seed = 557;
    char *texts[100];
    size_t lens[100];
    long words = 0;
    for (int g = 0; g < count; g++) {
        char *s = malloc(50100);
        size_t len = 0;
        while (len < 49980) {
            if (len > 0) s[len++] = ' ';
            int64_t length = 1 + next_random(&seed) % 12;
            for (int64_t k = 0; k < length; k++) s[len++] = (char)('!' + next_random(&seed) % 94);
            words++;
        }
        texts[g] = s;
        lens[g] = len;
    }
    int64_t checksum = 0;
    for (int round = 0; round < 50; round++) {
        for (int g = 0; g < count; g++) {
            int at = (round * 7 + g) % count;
            Str got = reverse_words(texts[at], lens[at]);
            unsigned char *b = (unsigned char *)got.p;
            checksum = (checksum * 31 + (int64_t)got.len + (int64_t)b[0] * 7 + (int64_t)b[got.len / 2]) % 1000000007;
            free(got.p);
        }
    }
    printf("%d texts, %ld words, 50 rounds each: checksum %lld\n", count, words, (long long)checksum);
    return 0;
}
