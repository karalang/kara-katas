// LeetCode #1451 Rearrange Words in a Sentence: the bench, a mirror of
// arrange_words.kara.
#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *text;
    size_t len;
} Word;

// merge sort by length, taking from the left on a tie, as a stable sort
// does
static void sort_words(Word *w, Word *tmp, size_t n) {
    if (n < 2) return;
    size_t mid = n / 2;
    sort_words(w, tmp, mid);
    sort_words(w + mid, tmp, n - mid);
    size_t i = 0, j = mid, k = 0;
    while (i < mid && j < n) tmp[k++] = w[j].len < w[i].len ? w[j++] : w[i++];
    while (i < mid) tmp[k++] = w[i++];
    while (j < n) tmp[k++] = w[j++];
    memcpy(w, tmp, n * sizeof *w);
}

// the words lowered, sorted by length with ties kept in order, joined, and
// the first letter raised, into a fresh string
static char *arrange_words(const char *text, size_t len) {
    size_t cap = 16, n = 0;
    Word *words = malloc(cap * sizeof *words);
    size_t start = 0;
    for (size_t i = 0; i <= len; i++) {
        if (i == len || text[i] == ' ') {
            if (n == cap) {
                cap *= 2;
                words = realloc(words, cap * sizeof *words);
            }
            size_t wl = i - start;
            char *w = malloc(wl);
            for (size_t k = 0; k < wl; k++) w[k] = (char)tolower((unsigned char)text[start + k]);
            words[n].text = w;
            words[n].len = wl;
            n++;
            start = i + 1;
        }
    }
    Word *tmp = malloc(n * sizeof *tmp);
    sort_words(words, tmp, n);
    char *out = malloc(len + 1);
    size_t at = 0;
    for (size_t i = 0; i < n; i++) {
        if (i > 0) out[at++] = ' ';
        memcpy(out + at, words[i].text, words[i].len);
        at += words[i].len;
        free(words[i].text);
    }
    out[at] = 0;
    out[0] = (char)toupper((unsigned char)out[0]);
    free(tmp);
    free(words);
    return out;
}

int main(void) {
    // 200 texts of 15000 words of 1 to 10 letters, the constraints' most,
    // each arranged and its letters folded to a checksum
    int64_t seed = 1451;
    int64_t check = 0;
    char *text = malloc(200000);
    for (int r = 0; r < 200; r++) {
        size_t len = 0;
        for (int i = 0; i < 15000; i++) {
            if (i > 0) text[len++] = ' ';
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t wl = 1 + seed / 65536 % 10;
            for (int64_t j = 0; j < wl; j++) {
                seed = (seed * 1103515245 + 12345) % 2147483648;
                char c = (char)('a' + seed / 65536 % 26);
                text[len++] = (i == 0 && j == 0) ? (char)toupper(c) : c;
            }
        }
        char *out = arrange_words(text, len);
        for (char *p = out; *p; p++) check = (check * 131 + (unsigned char)*p) % 1000000007;
        free(out);
    }
    free(text);
    printf("200 texts of 15000 words: checksum %lld\n", (long long)check);
    return 0;
}
