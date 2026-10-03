// Benchmark workload for LeetCode #336 — C mirror of palindrome_pairs.kara.
// C has no standard hash map, so this carries a small open-addressing table
// (FNV-1a, linear probing) keyed by the reversed words.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define WORDS 20000
#define PUNCHES 50
#define MODULUS 1073741789LL
#define SLOTS 65536 /* power of two, over twice WORDS */

typedef struct { char *s; int64_t len; } Str;
typedef struct { char *key; int64_t len; int64_t val; } Slot;
typedef struct { int64_t i, j; } Pair;

static uint64_t fnv(const char *s, int64_t n) {
    uint64_t h = 1469598103934665603ULL;
    for (int64_t k = 0; k < n; k++) h = (h ^ (uint8_t)s[k]) * 1099511628211ULL;
    return h;
}

static int64_t lookup(const Slot *t, const char *s, int64_t n) {
    uint64_t h = fnv(s, n) & (SLOTS - 1);
    while (t[h].key) {
        if (t[h].len == n && memcmp(t[h].key, s, n) == 0) return t[h].val;
        h = (h + 1) & (SLOTS - 1);
    }
    return -1;
}

static void insert(Slot *t, char *s, int64_t n, int64_t v) {
    uint64_t h = fnv(s, n) & (SLOTS - 1);
    while (t[h].key) {
        if (t[h].len == n && memcmp(t[h].key, s, n) == 0) { free(s); t[h].val = v; return; }
        h = (h + 1) & (SLOTS - 1);
    }
    t[h].key = s; t[h].len = n; t[h].val = v;
}

static int is_palindrome(const char *b, int64_t lo, int64_t hi) {
    int64_t i = lo, j = hi - 1;
    while (i < j) {
        if (b[i] != b[j]) return 0;
        i++; j--;
    }
    return 1;
}

static int cmp_pair(const void *a, const void *b) {
    const Pair *p = a, *q = b;
    if (p->i != q->i) return p->i < q->i ? -1 : 1;
    if (p->j != q->j) return p->j < q->j ? -1 : 1;
    return 0;
}

static Pair *pairs_buf; static int64_t pairs_len, pairs_cap;

static void push(int64_t i, int64_t j) {
    if (pairs_len == pairs_cap) {
        pairs_cap = pairs_cap ? pairs_cap * 2 : 16;
        pairs_buf = realloc(pairs_buf, sizeof(Pair) * pairs_cap);
    }
    pairs_buf[pairs_len++] = (Pair){i, j};
}

static void palindrome_pairs(const Str *words, int64_t n) {
    Slot *t = calloc(SLOTS, sizeof(Slot));
    for (int64_t i = 0; i < n; i++) {
        char *r = malloc(words[i].len + 1);
        for (int64_t k = 0; k < words[i].len; k++) r[k] = words[i].s[words[i].len - 1 - k];
        insert(t, r, words[i].len, i);
    }
    pairs_len = 0;
    for (int64_t i = 0; i < n; i++) {
        const char *w = words[i].s;
        int64_t len = words[i].len;
        for (int64_t k = 0; k <= len; k++) {
            if (is_palindrome(w, k, len)) {
                int64_t j = lookup(t, w, k);
                if (j >= 0 && j != i) push(i, j);
            }
            if (k > 0 && is_palindrome(w, 0, k)) {
                int64_t j = lookup(t, w + k, len - k);
                if (j >= 0 && j != i) push(j, i);
            }
        }
    }
    qsort(pairs_buf, pairs_len, sizeof(Pair), cmp_pair);
    for (int64_t h = 0; h < SLOTS; h++) free(t[h].key);
    free(t);
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const char *alphabet = "abc";
    int64_t seed = 336;
    Str *words = malloc(sizeof(Str) * WORDS);
    Slot *seen = calloc(SLOTS, sizeof(Slot));
    int64_t n = 0;
    while (n < WORDS) {
        int64_t len = 1 + next(&seed) % 10;
        char *w = malloc(len + 2);
        for (int64_t k = 0; k < len; k++) w[k] = alphabet[next(&seed) % 3];
        if (lookup(seen, w, len) < 0) {
            char *key = malloc(len);
            memcpy(key, w, len);
            insert(seen, key, len, n);
            words[n++] = (Str){w, len};
        } else {
            free(w);
        }
    }
    int64_t sink = 0;
    for (int64_t p = 0; p < PUNCHES; p++) {
        int64_t at = next(&seed) % WORDS;
        words[at].s[words[at].len] = 'd';
        words[at].len++;
        palindrome_pairs(words, n);
        words[at].len--;
        sink = (sink * 1000003 + pairs_len) % MODULUS;
        for (int64_t q = 0; q < pairs_len; q++)
            sink = (sink * 31 + pairs_buf[q].i * 7 + pairs_buf[q].j) % MODULUS;
    }
    printf("%lld\n", (long long)sink);
    for (int64_t h = 0; h < SLOTS; h++) free(seen[h].key);
    free(seen);
    for (int64_t i = 0; i < n; i++) free(words[i].s);
    free(words);
    free(pairs_buf);
    return 0;
}
