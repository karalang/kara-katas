// LeetCode #1816: Truncate Sentence -- the bench in C: the ★ arm over
// 2 * 10^6 calls on 1000 sentences of 20 to 100 words, built once, each
// sentence and its k drawn from the checksum so far. The words are split
// into an array of (start, length) and the first k joined into a new
// string, as the ★ arm's `split`, `take` and `join` do.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char *at;
    size_t len;
} Word;

static char *truncate_sentence(const char *s, int64_t k) {
    size_t cap = 8, n = 0;
    Word *w = malloc(cap * sizeof(Word));
    const char *start = s;
    for (const char *p = s; n < (size_t)k; p++) {
        if (*p == ' ' || *p == 0) {
            if (n == cap) {
                cap *= 2;
                w = realloc(w, cap * sizeof(Word));
            }
            w[n].at = start;
            w[n].len = (size_t)(p - start);
            n++;
            start = p + 1;
            if (*p == 0)
                break;
        }
    }
    size_t total = 0;
    for (size_t i = 0; i < n; i++)
        total += w[i].len + (i > 0);
    char *out = malloc(total + 1);
    size_t at = 0;
    for (size_t i = 0; i < n; i++) {
        if (i > 0)
            out[at++] = ' ';
        memcpy(out + at, w[i].at, w[i].len);
        at += w[i].len;
    }
    out[at] = 0;
    free(w);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1816;
    char *sentences[1000];
    int64_t words_in[1000];
    for (int i = 0; i < 1000; i++) {
        int64_t n = 20 + next_random(&seed) % 81;
        char *s = malloc(n * 6 + 1);
        size_t len = 0;
        for (int64_t w = 0; w < n; w++) {
            int64_t m = 1 + next_random(&seed) % 5;
            if (w > 0)
                s[len++] = ' ';
            for (int64_t c = 0; c < m; c++)
                s[len++] = (char)(97 + next_random(&seed) % 26);
        }
        s[len] = 0;
        sentences[i] = s;
        words_in[i] = n;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 2000000; call++) {
        int64_t i = (check + call) % 1000;
        char *cut = truncate_sentence(sentences[i], 1 + (check + call) % words_in[i]);
        check = (check * 31 + (int64_t)strlen(cut)) % 1000000007;
        free(cut);
    }
    printf("2000000 calls: checksum %lld\n", (long long)check);
    return 0;
}
