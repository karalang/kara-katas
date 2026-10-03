// Benchmark workload for LeetCode #331 — C mirror of verify_preorder.kara.
// Same tree, same variants, same punches, same sink. Tokens are scanned in
// place, between commas, as `strsep`-style views rather than copies.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NODES 100000
#define VARIANTS 16
#define PUNCHES 160
#define MODULUS 1073741789LL

static int is_valid_serialization(const char *s, size_t len) {
    int64_t slots = 1;
    size_t start = 0;
    for (size_t i = 0; i <= len; i++) {
        if (i == len || s[i] == ',') {
            if (slots == 0) return 0;
            if (i - start == 1 && s[start] == '#') slots -= 1;
            else slots += 1;
            start = i + 1;
        }
    }
    return slots == 0;
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245LL + 12345LL) % 2147483648LL;
    return *seed / 65536;
}

typedef struct { int *v; size_t len, cap; } Toks;  // -1 is '#', else a value

static void push(Toks *t, int x) {
    if (t->len == t->cap) {
        t->cap = t->cap ? t->cap * 2 : 1024;
        t->v = realloc(t->v, t->cap * sizeof(int));
    }
    t->v[t->len++] = x;
}

static void tree(int64_t *seed, int64_t n, Toks *out) {
    if (n == 0) { push(out, -1); return; }
    push(out, (int)(next(seed) % 100));
    int64_t left = next(seed) % n;
    tree(seed, left, out);
    tree(seed, n - 1 - left, out);
}

typedef struct { char *s; size_t len, cap; } Buf;

static void put(Buf *b, const char *x, size_t n) {
    while (b->len + n + 1 > b->cap) {
        b->cap = b->cap ? b->cap * 2 : 4096;
        b->s = realloc(b->s, b->cap);
    }
    memcpy(b->s + b->len, x, n);
    b->len += n;
}

static void put_tok(Buf *b, int x) {
    if (b->len) put(b, ",", 1);
    if (x < 0) { put(b, "#", 1); return; }
    char tmp[16];
    int n = snprintf(tmp, sizeof tmp, "%d", x);
    put(b, tmp, (size_t)n);
}

int main(void) {
    int64_t seed = 331;
    Toks toks = {0};
    tree(&seed, NODES, &toks);
    Buf variants[VARIANTS];
    for (int64_t v = 0; v < VARIANTS; v++) {
        int64_t kind = v % 4;
        int64_t hi = next(&seed);
        int64_t at = (hi * 32768 + next(&seed)) % (int64_t)toks.len;
        Buf b = {0};
        for (size_t i = 0; i < toks.len; i++) {
            if ((int64_t)i == at && kind == 1) continue;
            if ((int64_t)i == at && kind == 3) put_tok(&b, -1);
            if ((int64_t)i == at && kind == 2 && toks.v[i] < 0) { put_tok(&b, 7); put_tok(&b, -1); }
            put_tok(&b, toks.v[i]);
        }
        variants[v] = b;
    }
    int64_t sink = 0;
    for (int64_t p = 0; p < PUNCHES; p++) {
        int64_t v = next(&seed) % VARIANTS;
        int64_t answer = is_valid_serialization(variants[v].s, variants[v].len) ? 1 : 0;
        sink = (sink * 1000003 + answer * 64 + v) % MODULUS;
    }
    printf("%lld\n", (long long)sink);
    return 0;
}
