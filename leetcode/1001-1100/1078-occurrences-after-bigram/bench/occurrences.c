// LeetCode #1078 bench, C mirror of occurrences.kara: the same texts,
// bigrams, rounds and checksum. The words are views into the text (start
// and length); every answer is a malloc'd copy, as LeetCode's C signature
// returns them.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { const char *p; int64_t n; } View;

static int64_t seed = 1078;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int same(View w, const char *s, int64_t n) {
    return w.n == n && memcmp(w.p, s, (size_t)n) == 0;
}

// Returns the answers (malloc'd strings) and sets *count.
static char **find_occurrences(const char *text, int64_t tn, const char *first, int64_t fn,
                               const char *second, int64_t sn, int64_t *count) {
    int64_t cap = 16, nw = 0;
    View *words = malloc(sizeof(View) * (size_t)cap);
    int64_t start = 0;
    for (int64_t i = 0; i <= tn; i++) {
        if (i == tn || text[i] == ' ') {
            if (nw == cap) { cap *= 2; words = realloc(words, sizeof(View) * (size_t)cap); }
            words[nw].p = text + start;
            words[nw].n = i - start;
            nw++;
            start = i + 1;
        }
    }
    int64_t ocap = 4, no = 0;
    char **out = malloc(sizeof(char *) * (size_t)ocap);
    for (int64_t i = 2; i < nw; i++) {
        if (same(words[i - 2], first, fn) && same(words[i - 1], second, sn)) {
            if (no == ocap) { ocap *= 2; out = realloc(out, sizeof(char *) * (size_t)ocap); }
            char *w = malloc((size_t)words[i].n + 1);
            memcpy(w, words[i].p, (size_t)words[i].n);
            w[words[i].n] = 0;
            out[no++] = w;
        }
    }
    free(words);
    *count = no;
    return out;
}

static char *random_word(int64_t longest, int64_t k) {
    int64_t n = next_random() % longest + 1;
    char *s = malloc((size_t)n + 1);
    for (int64_t i = 0; i < n; i++) s[i] = (char)('a' + next_random() % k);
    s[n] = 0;
    return s;
}

int main(void) {
    const int64_t rounds = 300;
    char *vocabulary[12];
    for (int i = 0; i < 12; i++) vocabulary[i] = random_word(4, 3);
    char *texts[100];
    int64_t text_len[100];
    const char *firsts[800], *seconds[800];
    int64_t owner[800];
    int64_t queries = 0;
    for (int64_t t = 0; t < 100; t++) {
        const char *words[1000];
        int64_t nw = 0, length = -1;
        for (;;) {
            const char *w = vocabulary[next_random() % 12];
            int64_t wl = (int64_t)strlen(w);
            if (length + 1 + wl > 1000) break;
            length += 1 + wl;
            words[nw++] = w;
        }
        for (int q = 0; q < 8; q++) {
            if (next_random() % 4 < 3) {
                int64_t at = next_random() % (nw - 1);
                firsts[queries] = words[at];
                seconds[queries] = words[at + 1];
            } else {
                firsts[queries] = vocabulary[next_random() % 12];
                seconds[queries] = vocabulary[next_random() % 12];
            }
            owner[queries] = t;
            queries++;
        }
        char *s = malloc((size_t)length + 1);
        int64_t at = 0;
        for (int64_t i = 0; i < nw; i++) {
            if (i > 0) s[at++] = ' ';
            int64_t wl = (int64_t)strlen(words[i]);
            memcpy(s + at, words[i], (size_t)wl);
            at += wl;
        }
        s[at] = 0;
        texts[t] = s;
        text_len[t] = at;
    }
    int64_t found = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t j = 0; j < queries; j++) {
            int64_t q = (j * 7 + r) % queries;
            int64_t n;
            char **out = find_occurrences(texts[owner[q]], text_len[owner[q]], firsts[q],
                                          (int64_t)strlen(firsts[q]), seconds[q],
                                          (int64_t)strlen(seconds[q]), &n);
            found += n;
            for (int64_t i = 0; i < n; i++) {
                for (const char *c = out[i]; *c; c++) check = (check * 31 + (unsigned char)*c) % 1000000007;
                free(out[i]);
            }
            free(out);
            check = (check * 31 + n) % 1000000007;
        }
    }
    printf("%lld rounds of %lld bigrams over 100 texts: %lld words found, checksum %lld\n",
           (long long)rounds, (long long)queries, (long long)found, (long long)check);
    return 0;
}
