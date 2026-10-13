// Benchmark for #535: C mirror of the ★ arm (a counter written in base
// 62); see encode_and_decode_tinyurl.kara. C has no map, so each codec
// holds two open-addressing tables (FNV-1a over the bytes, linear
// probing, doubled at half full) that own copies of their keys and
// values, as the ★ arm's two `Map[String, String]` do. `encode` returns
// a fresh short URL and `decode` a fresh copy of the URL, as the ★ arm's
// `String` results are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PREFIX "http://tinyurl.com/"
#define PREFIX_LEN 19

typedef struct {
    char *s;
    int64_t n;
} Str;

static Str copy(const char *s, int64_t n) {
    Str out = {malloc(n + 1), n};
    memcpy(out.s, s, n);
    out.s[n] = 0;
    return out;
}

static uint64_t fnv(const char *s, int64_t n) {
    uint64_t h = 1469598103934665603ULL;
    for (int64_t i = 0; i < n; i++) h = (h ^ (unsigned char)s[i]) * 1099511628211ULL;
    return h;
}

typedef struct {
    Str *keys;
    Str *values;
    uint64_t size, len;
} Table;

static void table_init(Table *t) {
    t->size = 8;
    t->len = 0;
    t->keys = calloc(t->size, sizeof(Str));
    t->values = calloc(t->size, sizeof(Str));
}

static uint64_t table_slot(const Table *t, const char *k, int64_t n) {
    uint64_t i = fnv(k, n) & (t->size - 1);
    while (t->keys[i].s && (t->keys[i].n != n || memcmp(t->keys[i].s, k, n) != 0)) i = (i + 1) & (t->size - 1);
    return i;
}

static const Str *table_get(const Table *t, const char *k, int64_t n) {
    uint64_t i = table_slot(t, k, n);
    return t->keys[i].s ? &t->values[i] : NULL;
}

// Inserts a key that is not in the table; the table takes both strings.
static void table_insert(Table *t, Str k, Str v) {
    if (2 * (t->len + 1) > t->size) {
        Table bigger = {calloc(2 * t->size, sizeof(Str)), calloc(2 * t->size, sizeof(Str)), 2 * t->size, t->len};
        for (uint64_t i = 0; i < t->size; i++) {
            if (!t->keys[i].s) continue;
            uint64_t j = table_slot(&bigger, t->keys[i].s, t->keys[i].n);
            bigger.keys[j] = t->keys[i];
            bigger.values[j] = t->values[i];
        }
        free(t->keys);
        free(t->values);
        *t = bigger;
    }
    uint64_t i = table_slot(t, k.s, k.n);
    t->keys[i] = k;
    t->values[i] = v;
    t->len++;
}

static void table_free(Table *t) {
    for (uint64_t i = 0; i < t->size; i++) {
        if (!t->keys[i].s) continue;
        free(t->keys[i].s);
        free(t->values[i].s);
    }
    free(t->keys);
    free(t->values);
}

static char digit(int64_t d) {
    if (d < 10) return (char)('0' + d);
    if (d < 36) return (char)('a' + d - 10);
    return (char)('A' + d - 36);
}

static Str base62(int64_t n) {
    char rev[16];
    int64_t k = 0;
    int64_t m = n;
    for (;;) {
        rev[k++] = digit(m % 62);
        m /= 62;
        if (m == 0) break;
    }
    Str code = {malloc(k + 1), k};
    for (int64_t i = 0; i < k; i++) code.s[i] = rev[k - 1 - i];
    code.s[k] = 0;
    return code;
}

typedef struct {
    Table by_code, by_url;
    int64_t next;
} Codec;

static void codec_init(Codec *c) {
    table_init(&c->by_code);
    table_init(&c->by_url);
    c->next = 0;
}

static Str encode(Codec *c, const Str *long_url) {
    const Str *found = table_get(&c->by_url, long_url->s, long_url->n);
    Str code;
    if (found) {
        code = copy(found->s, found->n);
    } else {
        code = base62(c->next);
        c->next++;
        table_insert(&c->by_code, copy(code.s, code.n), copy(long_url->s, long_url->n));
        table_insert(&c->by_url, copy(long_url->s, long_url->n), copy(code.s, code.n));
    }
    Str out = {malloc(PREFIX_LEN + code.n + 1), PREFIX_LEN + code.n};
    memcpy(out.s, PREFIX, PREFIX_LEN);
    memcpy(out.s + PREFIX_LEN, code.s, code.n + 1);
    free(code.s);
    return out;
}

static Str decode(const Codec *c, const Str *short_url) {
    const Str *url = table_get(&c->by_code, short_url->s + PREFIX_LEN, short_url->n - PREFIX_LEN);
    return copy(url->s, url->n);
}

static int64_t seed = 535;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static Str random_url(int64_t most) {
    const char *marks = "/-_.?=&";
    char buf[256];
    int64_t n = 0;
    memcpy(buf, "https://", 8);
    n = 8;
    int64_t host = 3 + next_random() % 8;
    for (int64_t i = 0; i < host; i++) buf[n++] = (char)('a' + next_random() % 26);
    memcpy(buf + n, ".com/", 5);
    n += 5;
    int64_t path = next_random() % (most + 1);
    for (int64_t i = 0; i < path; i++) {
        int64_t k = next_random() % 69;
        if (k < 26) buf[n++] = (char)('a' + k);
        else if (k < 52) buf[n++] = (char)('A' + k - 26);
        else if (k < 62) buf[n++] = (char)('0' + k - 52);
        else buf[n++] = marks[k - 62];
    }
    return copy(buf, n);
}

int main(void) {
    enum { N = 20000 };
    static Str urls[N];
    static Str shorts[N];
    for (int64_t i = 0; i < N; i++) {
        if (i % 5 == 4) {
            int64_t j = next_random() % i;
            urls[i] = copy(urls[j].s, urls[j].n);
        } else {
            urls[i] = random_url(100);
        }
    }
    int64_t rounds = 50;
    int64_t right = 0;
    int64_t length = 0;
    for (int64_t r = 0; r < rounds; r++) {
        Codec codec;
        codec_init(&codec);
        for (int64_t i = 0; i < N; i++) {
            shorts[i] = encode(&codec, &urls[i]);
            length += shorts[i].n;
        }
        for (int64_t i = 0; i < N; i++) {
            Str back = decode(&codec, &shorts[i]);
            if (back.n == urls[i].n && memcmp(back.s, urls[i].s, back.n) == 0) right++;
            free(back.s);
        }
        for (int64_t i = 0; i < N; i++) free(shorts[i].s);
        table_free(&codec.by_code);
        table_free(&codec.by_url);
    }
    printf("%d URLs, %lld rounds: %lld back, short length %lld\n", N, (long long)rounds, (long long)right, (long long)length);
    for (int64_t i = 0; i < N; i++) free(urls[i].s);
    return 0;
}
