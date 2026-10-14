// Benchmark for #591: C mirror of the ★ arm (one scan with a stack of
// open tags); see tag_validator.kara. The stack holds a malloc'd copy of
// each open tag's name, as the Kāra arm's holds `String`s, and is freed
// at the end of each call.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int starts(const char *s, int64_t n, int64_t i, const char *w) {
    int64_t m = (int64_t)strlen(w);
    return i + m <= n && memcmp(s + i, w, m) == 0;
}

// Index of `w` in s from `from`, or -1.
static int64_t find(const char *s, int64_t n, int64_t from, const char *w) {
    int64_t m = (int64_t)strlen(w);
    for (int64_t i = from; i + m <= n; i++)
        if (memcmp(s + i, w, m) == 0) return i;
    return -1;
}

static int valid_name(const char *s, int64_t len) {
    if (len < 1 || len > 9) return 0;
    for (int64_t i = 0; i < len; i++)
        if (s[i] < 'A' || s[i] > 'Z') return 0;
    return 1;
}

typedef struct {
    char **names;
    int64_t len, cap;
} Stack;

static int finish(Stack *st, int ok) {
    for (int64_t k = 0; k < st->len; k++) free(st->names[k]);
    free(st->names);
    return ok;
}

static int is_valid(const char *code, int64_t n) {
    Stack st = {NULL, 0, 0};
    int64_t i = 0;
    while (i < n) {
        if (i > 0 && st.len == 0) return finish(&st, 0);
        if (starts(code, n, i, "<![CDATA[")) {
            if (st.len == 0) return finish(&st, 0);
            int64_t k = find(code, n, i + 9, "]]>");
            if (k < 0) return finish(&st, 0);
            i = k + 3;
        } else if (starts(code, n, i, "</")) {
            int64_t start = i + 2, k = find(code, n, start, ">");
            if (k < 0) return finish(&st, 0);
            int64_t len = k - start;
            if (st.len == 0) return finish(&st, 0);
            char *top = st.names[st.len - 1];
            if ((int64_t)strlen(top) != len || memcmp(top, code + start, len) != 0) return finish(&st, 0);
            free(top);
            st.len--;
            i = k + 1;
        } else if (code[i] == '<') {
            int64_t start = i + 1, k = find(code, n, start, ">");
            if (k < 0) return finish(&st, 0);
            int64_t len = k - start;
            if (!valid_name(code + start, len)) return finish(&st, 0);
            if (st.len == st.cap) {
                st.cap = st.cap ? st.cap * 2 : 4;
                st.names = realloc(st.names, st.cap * sizeof(char *));
            }
            char *name = malloc(len + 1);
            memcpy(name, code + start, len);
            name[len] = 0;
            st.names[st.len++] = name;
            i = k + 1;
        } else {
            if (st.len == 0) return finish(&st, 0);
            i++;
        }
    }
    return finish(&st, st.len == 0);
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char buf[1 << 20];

static void snippet(int64_t depth, int64_t *seed, char *out, int64_t *len) {
    static const char *names[] = {"A", "XY", "ABCDEFGHI", "CODE"};
    static const char *texts[] = {"x", " ", ">", "]]>", "!", "[", "y", "/", "...", "<![CDATA[<A>]]>"};
    const char *name = names[step(seed) % 4];
    *len += sprintf(out + *len, "<%s>", name);
    int64_t parts = step(seed) % 7;
    for (int64_t p = 0; p < parts; p++) {
        if (step(seed) % 10 < 4 && depth > 0) {
            snippet(depth - 1, seed, out, len);
        } else {
            *len += sprintf(out + *len, "%s", texts[step(seed) % 10]);
        }
    }
    if (step(seed) % 40 == 0)
        *len += sprintf(out + *len, "</B>");
    else
        *len += sprintf(out + *len, "</%s>", name);
}

int main(void) {
    enum { COUNT = 1000, ROUNDS = 1000 };
    int64_t seed = 591;
    static char *codes[COUNT];
    static int64_t lens[COUNT];
    int got = 0;
    while (got < COUNT) {
        int64_t len = 0;
        snippet(4, &seed, buf, &len);
        if (len >= 200 && len <= 500) {
            codes[got] = malloc(len + 1);
            memcpy(codes[got], buf, len + 1);
            lens[got++] = len;
        }
    }
    int64_t valid = 0, checksum = 0;
    for (int round = 0; round < ROUNDS; round++)
        for (int g = 0; g < COUNT; g++) {
            int64_t c = (round * 7 + g) % COUNT;
            if (is_valid(codes[c], lens[c])) {
                valid++;
                checksum = (checksum * 31 + g + 1) % 1000000007;
            }
        }
    printf("%d snippets, %d rounds: %lld valid, checksum %lld\n", COUNT, ROUNDS, (long long)valid,
           (long long)checksum);
    return 0;
}
