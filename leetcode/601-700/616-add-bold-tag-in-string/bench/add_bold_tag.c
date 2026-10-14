// Benchmark for #616: the ★ arm (mark, then write); see
// add_bold_tag.kara. Each call marks the characters with a `malloc`'d
// array, tests each word at each position with `strncmp`, writes into a
// `malloc`'d buffer that doubles as it fills, and frees the marks; the
// caller frees the string. The words' lengths are taken once a call, as
// the other languages' strings carry theirs.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *buf;
    size_t len, cap;
} Out;

static void put(Out *o, const char *s, size_t n) {
    if (o->len + n + 1 > o->cap) {
        while (o->len + n + 1 > o->cap) o->cap = o->cap ? 2 * o->cap : 16;
        o->buf = realloc(o->buf, o->cap);
    }
    memcpy(o->buf + o->len, s, n);
    o->len += n;
    o->buf[o->len] = 0;
}

static char *add_bold_tag(const char *s, char **words, size_t count, size_t *len) {
    size_t n = strlen(s);
    char *bold = calloc(n ? n : 1, 1);
    size_t *sizes = malloc(count * sizeof(size_t));
    for (size_t w = 0; w < count; w++) sizes[w] = strlen(words[w]);
    for (size_t i = 0; i < n; i++)
        for (size_t w = 0; w < count; w++) {
            size_t m = sizes[w];
            if (m <= n - i && strncmp(s + i, words[w], m) == 0)
                for (size_t k = i; k < i + m; k++) bold[k] = 1;
        }
    Out o = {0};
    for (size_t i = 0; i < n; i++) {
        if (bold[i] && (i == 0 || !bold[i - 1])) put(&o, "<b>", 3);
        put(&o, s + i, 1);
        if (bold[i] && (i == n - 1 || !bold[i + 1])) put(&o, "</b>", 4);
    }
    if (!o.buf) put(&o, "", 0);
    free(bold);
    free(sizes);
    *len = o.len;
    return o.buf;
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char *random_text(int64_t size, int64_t *seed) {
    char *t = malloc((size_t)size + 1);
    for (int64_t k = 0; k < size; k++) t[k] = (char)(97 + step(seed) % 4);
    t[size] = 0;
    return t;
}

int main(void) {
    enum { CASES = 20, ROUNDS = 1000, WORDS = 100 };
    int64_t seed = 616;
    static char *texts[CASES];
    static char *lists[CASES][WORDS];
    for (int c = 0; c < CASES; c++) {
        char *s = random_text(1000, &seed);
        int count = 0;
        while (count < WORDS) {
            int64_t length = 5 + step(&seed) % 10;
            char *w;
            if (count % 2 == 0) {
                int64_t at = step(&seed) % (1000 - length);
                w = malloc((size_t)length + 1);
                memcpy(w, s + at, (size_t)length);
                w[length] = 0;
            } else {
                w = random_text(length, &seed);
            }
            int seen = 0;
            for (int k = 0; k < count; k++)
                if (strcmp(lists[c][k], w) == 0) seen = 1;
            if (seen)
                free(w);
            else
                lists[c][count++] = w;
        }
        texts[c] = s;
    }
    int64_t total = 0, checksum = 0;
    for (int r = 0; r < ROUNDS; r++) {
        int c = (r * 7) % CASES;
        size_t len;
        char *out = add_bold_tag(texts[c], lists[c], WORDS, &len);
        total += (int64_t)len;
        for (size_t k = 0; k < len; k++) checksum = (checksum * 31 + (unsigned char)out[k]) % 1000000007;
        free(out);
    }
    printf("%d cases, %d rounds: %lld characters, checksum %lld\n", CASES, ROUNDS, (long long)total,
           (long long)checksum);
    return 0;
}
